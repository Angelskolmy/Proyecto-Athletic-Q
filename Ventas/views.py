from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from django.http import JsonResponse
from decimal import Decimal

from .models import Venta
from .forms import VentaForm
from Detalle_venta.models import Detalle_Venta
from Productos.models import producto
from Empleados.models import User_Empleados
from Categorias.models import categoria
from Historial_ventas.models import Historial_Ventas


@login_required(login_url='login')
@permission_required('Ventas.add_venta', login_url='home')
def ListarVentas(request):
    
    empleado = request.user
    hoy = timezone.now().date()
    
    # Obtener ventas del empleado en el día
    ventas_hoy = Venta.objects.filter(
        id_usuario=empleado,
        Fecha__date=hoy
    )
    
    # Calcular estadísticas
    stats = ventas_hoy.aggregate(
        total_ventas=Count('Id_venta'),
        total_recaudado=Sum('Total')
    )
    
    total_ventas = stats['total_ventas'] or 0
    total_recaudado = stats['total_recaudado'] or Decimal('0.00')
    
    # Datos para formulario
    empleados = User_Empleados.objects.filter(is_active=True, is_staff=True).order_by('first_name')
    productos = producto.objects.filter(Estado='Activo').select_related('Catego_Id').order_by('Nombre')
    categorias = categoria.objects.filter(Estado='Activo').order_by('Nombre')

    # <<< CAMBIO: crear form y pasarlo al contexto >>>
    form = VentaForm(initial={'id_usuario': empleado.id})
    
    context = {
        'empleado': empleado,
        'total_ventas': total_ventas,
        'total_recaudado': total_recaudado,
        'empleados': empleados,
        'productos': productos,
        'categorias': categorias,
        'hoy': hoy,
        'form': form,  # <-- agregado
    }
    
    return render(request, "templates_ventas/ventas.html", context)

@login_required(login_url='login')
@permission_required('Ventas.add_venta', login_url='Ventas')
@transaction.atomic
def ProcesarVenta(request):
    if request.method != 'POST':
        messages.error(request, 'Método no permitido')
        return redirect('Ventas')

    form = VentaForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Datos inválidos en el formulario')
        return redirect('Ventas')

    try:
        # Productos enviados por JS
        productos_ids = request.POST.getlist('producto_id[]')
        cantidades = request.POST.getlist('cantidad[]')
        if not productos_ids:
            messages.error(request, 'Debe agregar al menos un producto')
            return redirect('Ventas')

        # Calcular total y validar stock
        total = Decimal('0.00')
        items = []
        for i in range(len(productos_ids)):
            prod = get_object_or_404(producto, Id_producto=productos_ids[i])
            cantidad = int(cantidades[i])
            if prod.Stock < cantidad:
                messages.error(request, f'Stock insuficiente para {prod.Nombre}')
                return redirect('Ventas')
            subtotal = prod.Precio_de_venta * cantidad
            total += subtotal
            items.append({'producto': prod, 'cantidad': cantidad, 'subtotal': subtotal})

        # Guardar venta
        venta = form.save(commit=False)
        venta.Total = total
        venta.save()

        # Crear detalles y descontar stock
        metodo_pago = form.cleaned_data.get('metodo_pago')
        for item in items:
            p = item['producto']
            p.Stock -= item['cantidad']
            p.save()
            Detalle_Venta.objects.create(
                Id_venta=venta,
                Id_producto=p,
                Tipo_Pago=metodo_pago,
                Cantidad=item['cantidad'],
                Subtotal=item['subtotal'],
                Total=total
            )

        # Registrar historial
        hist = Historial_Ventas.objects.create(
            id_usuario=venta.id_usuario,
            id_venta=venta,
            Monto=total,
            metodo_pago=metodo_pago
        )

        # Obtener cedula ingresada
        cedula_vents = form.cleaned_data.get('Cedula_Vents')
        
        # Buscar si existe cliente con esa cedula
        cliente_usuario = None
        if cedula_vents:
            cliente_usuario = User_Empleados.objects.filter(Cedula=cedula_vents).first()
        
        # Si no existe, usar usuario fantasma (ID 37)
        if not cliente_usuario:
            try:
                cliente_usuario = User_Empleados.objects.get(pk=37)
            except User_Empleados.DoesNotExist:
                cliente_usuario = None
        
        # Intentar asignar el cliente al historial si tiene ese campo
        if cliente_usuario:
            for campo_posible in ('id_cliente', 'cliente', 'id_usuario_cliente', 'usuario_cliente'):
                if hasattr(hist, campo_posible):
                    setattr(hist, campo_posible, cliente_usuario)
                    hist.save()
                    break

        messages.success(request, f'Venta #{venta.Id_venta} creada - Total: ${total:,.0f}')
        return redirect('Ventas')

    except Exception as e:
        transaction.set_rollback(True)
        messages.error(request, f'Error: {str(e)}')
        return redirect('Ventas')


@login_required(login_url='login')
@permission_required('Ventas.view_venta', login_url='Ventas')
def DetalleVenta(request, id):
    
    venta = get_object_or_404(
        Venta.objects.select_related('id_usuario'),
        Id_venta=id
    )
    
    detalles = Detalle_Venta.objects.filter(
        Id_venta=venta
    ).select_related('Id_producto__Catego_Id')
    
    total_items = sum(detalle.Cantidad for detalle in detalles)
    subtotal_sin_iva = venta.Total / Decimal('1.19')
    iva = venta.Total - subtotal_sin_iva
    
    context = {
        'venta': venta,
        'detalles': detalles,
        'total_items': total_items,
        'subtotal_sin_iva': subtotal_sin_iva,
        'iva': iva,
    }
    
    return render(request, 'templates_ventas/detalle_venta.html', context)


@login_required(login_url='login')
@permission_required('Ventas.change_venta', login_url='Ventas')
def EditarVenta(request, id):
    """Editar venta - SOLO ADMIN"""
    
    venta = get_object_or_404(Venta, Id_venta=id)
    detalles = Detalle_Venta.objects.filter(Id_venta=venta).select_related('Id_producto__Catego_Id')
    
    empleados = User_Empleados.objects.filter(is_active=True, is_staff=True).order_by('first_name')
    productos = producto.objects.filter(Estado='Activo').select_related('Catego_Id').order_by('Nombre')
    categorias = categoria.objects.filter(Estado='Activo').order_by('Nombre')
    
    # Preparar carrito con los productos actuales
    carrito_inicial = []
    for detalle in detalles:
        carrito_inicial.append({
            'id': detalle.Id_producto.Id_producto,
            'nombre': detalle.Id_producto.Nombre,
            'precio': float(detalle.Id_producto.Precio_de_venta),
            'cantidad': detalle.Cantidad,
            'stock': detalle.Id_producto.Stock + detalle.Cantidad
        })
    
    return render(request, 'templates_ventas/editar_ventas.html', {
        'venta': venta,
        'detalles': detalles,
        'empleados': empleados,
        'productos': productos,
        'categorias': categorias,
        'carrito_inicial': carrito_inicial,
    })


@login_required(login_url='login')
@permission_required('Ventas.change_venta', login_url='Ventas')
@transaction.atomic
def ActualizarVenta(request, id):
    """Actualizar venta existente"""
    
    if request.method != 'POST':
        messages.error(request, 'Método no permitido')
        return redirect('Ventas')
    
    try:
        venta = get_object_or_404(Venta, Id_venta=id)
        detalles_anteriores = Detalle_Venta.objects.filter(Id_venta=venta)
        
        # Restaurar stock de productos anteriores
        for detalle in detalles_anteriores:
            detalle.Id_producto.Stock += detalle.Cantidad
            detalle.Id_producto.save()
        
        # Eliminar detalles anteriores
        detalles_anteriores.delete()
        
        # Obtener nuevos datos
        metodo_pago = request.POST.get('metodo_pago', 'Efectivo')
        observaciones = request.POST.get('observaciones', '')
        
        productos_ids = request.POST.getlist('producto_id[]')
        cantidades = request.POST.getlist('cantidad[]')
        
        if not productos_ids:
            messages.error(request, 'Debe agregar al menos un producto')
            return redirect('editar_venta', id=id)
        
        # Calcular nuevo total
        total = Decimal('0.00')
        
        for i in range(len(productos_ids)):
            prod = get_object_or_404(producto, Id_producto=productos_ids[i])
            cantidad = int(cantidades[i])
            
            if prod.Stock < cantidad:
                messages.error(request, f'Stock insuficiente para {prod.Nombre}')
                return redirect('editar_venta', id=id)
            
            subtotal = prod.Precio_de_venta * cantidad
            total += subtotal
            
            # Descontar nuevo stock
            prod.Stock -= cantidad
            prod.save()
            
            # Crear nuevo detalle
            Detalle_Venta.objects.create(
                Id_venta=venta,
                Id_producto=prod,
                Tipo_Pago=metodo_pago,
                Cantidad=cantidad,
                Subtotal=subtotal,
                Total=total
            )
        
        # Actualizar venta
        venta.Total = total
        venta.observaciones_edicion = observaciones
        venta.save()
        
        messages.success(request, f' Venta #{venta.Id_venta} actualizada exitosamente')
        return redirect('detalle_venta', id=venta.Id_venta)
        
    except Exception as e:
        messages.error(request, f' Error: {str(e)}')
        return redirect('editar_venta', id=id)