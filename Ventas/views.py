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
from django.utils import timezone  
from Historial.models import Historial_usuario


@login_required(login_url='login')
@permission_required('Ventas.add_venta', login_url='home')
def ListarVentas(request):
    """Vista principal de ventas con estadísticas del empleado"""
    
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
    
    context = {
        'empleado': empleado,
        'total_ventas': total_ventas,
        'total_recaudado': total_recaudado,
        'empleados': empleados,
        'productos': productos,
        'categorias': categorias,
        'hoy': hoy,
    }
    
    return render(request, "templates_ventas/ventas.html", context)

@login_required(login_url='login')
@permission_required('Ventas.add_venta', login_url='Ventas')
@transaction.atomic
def ProcesarVenta(request):
    """Procesar nueva venta"""
    
    if request.method != 'POST':
        messages.error(request, 'Método no permitido')
        return redirect('Ventas')
    
    try:
        # 1. OBTENER VENDEDOR
        empleado_id = request.POST.get('empleado_id')
        
        # Validar que empleado_id no esté vacío
        if not empleado_id:
            messages.error(request, 'Debe seleccionar un vendedor')
            return redirect('Ventas')
        
        empleado = get_object_or_404(User_Empleados, id=empleado_id)
        
        # 2. OBTENER MÉTODO DE PAGO
        metodo_pago = request.POST.get('metodo_pago', 'Efectivo')
        
        # 3. OBTENER PRODUCTOS
        productos_ids = request.POST.getlist('producto_id[]')
        cantidades = request.POST.getlist('cantidad[]')
        
        if not productos_ids:
            messages.error(request, 'Debe agregar al menos un producto')
            return redirect('Ventas')
        
        # 4. CALCULAR TOTAL
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
            
            items.append({
                'producto': prod,
                'cantidad': cantidad,
                'precio': prod.Precio_de_venta,
                'subtotal': subtotal
            })
        
        # 5. CREAR VENTA
        venta = Venta.objects.create(
            id_usuario=empleado,
            Total=total
        )
        
        # 6. CREAR DETALLES Y DESCONTAR STOCK
        for item in items:
            item['producto'].Stock -= item['cantidad']
            item['producto'].save()
            
            Detalle_Venta.objects.create(
                Id_venta=venta,
                Id_producto=item['producto'],
                Tipo_Pago=metodo_pago,
                Cantidad=item['cantidad'],
                Subtotal=item['subtotal'],
                Total=total
            )
        
        # 7. REGISTRAR EN HISTORIAL
        Historial_Ventas.objects.create(
            id_usuario=empleado,
            id_venta=venta,
            Monto=total,
            metodo_pago=metodo_pago
        ) 

        histVend = empleado
        histMod = 'ventas'
        histMovs = 'ingresar'
        histFech = timezone.now().date()             
        histNomb = f"Venta #{venta.Id_venta}"[:50]  
        histId = int(venta.Id_venta)

        try:
            hu = Historial_usuario.objects.create(
                id_usuario=histVend,
                TIpo_Movimiento=histMovs,
                Modulo=histMod,
                Nombre_Objeto=histNomb,
                Id_Objeto=histId,
                Fecha_y_hora=histFech,
            )
            print("DEBUG: Historial_usuario created Id_historial =", getattr(hu, 'Id_historial', None))
        except Exception as exc:
            import traceback
            traceback.print_exc()
            messages.warning(request, f' No se pudo registrar en historial de movimientos: {exc}')

        messages.success(request, f' Venta #{venta.Id_venta} creada - Total: ${total:,.0f}')
        return redirect('Ventas')
        
    except Exception as e:
        messages.error(request, f' Error: {str(e)}')
        return redirect('Ventas')


@login_required(login_url='login')
@permission_required('Ventas.view_venta', login_url='Ventas')
def DetalleVenta(request, id):
    """Ver detalle de una venta"""
    
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

        histVend2 = request.user
        histMod2 = 'ventas'
        histMovs2 = 'editar'
        histFech2 = timezone.now().date()             
        histNomb2 = f"Venta #{venta.Id_venta}"[:50]  
        histId2 = int(venta.Id_venta) 

        try:
            hu = Historial_usuario.objects.create(
                id_usuario=histVend2,
                TIpo_Movimiento=histMovs2,
                Modulo=histMod2,
                Nombre_Objeto=histNomb2,
                Id_Objeto=histId2,
                Fecha_y_hora=histFech2,
            )
            print("DEBUG: Historial_usuario created Id_historial =", getattr(hu, 'Id_historial', None))
        except Exception as exc:
            import traceback
            traceback.print_exc()   # ver error real en la consola
            messages.warning(request, f' No se pudo registrar en historial de movimientos: {exc}')

        
        messages.success(request, f' Venta #{venta.Id_venta} actualizada exitosamente')
        return redirect('detalle_venta', id=venta.Id_venta)
        
    except Exception as e:
        messages.error(request, f' Error: {str(e)}')
        return redirect('editar_venta', id=id)