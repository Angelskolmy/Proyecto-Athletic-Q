from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from decimal import Decimal

from .models import Venta
from .forms import VentaForm
from Detalle_venta.models import Detalle_Venta
from Productos.models import producto
from Empleados.models import User_Empleados
from Categorias.models import categoria


@login_required(login_url='login')
@permission_required('Ventas.view_venta', login_url='home')
def ListarVentas(request):
    """Lista simple de ventas"""
    ventas = Venta.objects.select_related('id_usuario').all().order_by('-Fecha')
    
    return render(request, "templates_ventas/ventas.html", {'Ventas': ventas})


@login_required(login_url='login')
@permission_required('Ventas.add_venta', login_url='Ventas')
def CrearVentas(request):
    
    # Datos para el formulario
    form = VentaForm()
    empleados = User_Empleados.objects.filter(is_active=True, is_staff=True).order_by('first_name')
    productos = producto.objects.filter(Estado='Activo').select_related('Catego_Id').order_by('Nombre')
    categorias = categoria.objects.filter(Estado='Activo').order_by('Nombre')
    
    context = {
        'form': form,
        'empleados': empleados,
        'productos': productos,
        'categorias': categorias,
    }
    
    return render(request, 'templates_ventas/crear_ventas.html', context)


@login_required(login_url='login')
@permission_required('Ventas.add_venta', login_url='Ventas')
@transaction.atomic
def ProcesarVenta(request):
    
    if request.method != 'POST':
        messages.error(request, 'Método no permitido')
        return redirect('Ventas')
    
    try:
        # 1. OBTENER VENDEDOR
        empleado_id = request.POST.get('empleado_id')
        empleado = get_object_or_404(User_Empleados, id=empleado_id)
        
        # 2. OBTENER MÉTODO DE PAGO
        metodo_pago = request.POST.get('metodo_pago', 'Efectivo')
        
        # 3. OBTENER PRODUCTOS Y CANTIDADES
        productos_ids = request.POST.getlist('producto_id[]')
        cantidades = request.POST.getlist('cantidad[]')
        
        #condicion por si el carrito esta vacio
        if not productos_ids:
            messages.error(request, 'Debe agregar al menos un producto')
            return redirect('ventas_create')
        
        # 4. Calcular total
        total = Decimal('0.00')
        items = []
        
        # Recorrer cada producto del carrito
        for i in range(len(productos_ids)):
            prod = get_object_or_404(producto, Id_producto=productos_ids[i])
            cantidad = int(cantidades[i])
            
            # Validar stock
            if prod.Stock < cantidad:
                messages.error(request, f'Stock insuficiente para {prod.Nombre}')
                return redirect('ventas_create')
            
            # Calcular subtotal
            subtotal = prod.Precio_de_venta * cantidad
            total += subtotal
            
            # Guardar info en la lista temporal
            items.append({
                'producto': prod,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
        
        # Crear venta en la tabla
        venta = Venta.objects.create(
            id_usuario=empleado,
            Total=total
        )
        
        # Crear detalle venta
        for item in items:
            Detalle_Venta.objects.create(
                Id_venta=venta,
                Id_producto=item['producto'],
                Tipo_Pago=metodo_pago,
                Cantidad=item['cantidad'],
                Subtotal=item['subtotal'],
                Total=total
            )
            
            # Descontar stock
            item['producto'].Stock -= item['cantidad']
            item['producto'].save()
        
        messages.success(request, f'Venta #{venta.Id_venta} creada exitosamente')
        return redirect('Ventas')
        
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('ventas_create')


@login_required(login_url='login')
@permission_required('Ventas.view_venta', login_url='Ventas')
def DetalleVenta(request, id):
    """Ver detalle completo de una venta"""
    
    # Obtener venta con relaciones
    venta = get_object_or_404(
        Venta.objects.select_related('id_usuario'),
        Id_venta=id
    )
    
    # Obtener detalles de la venta
    detalles = Detalle_Venta.objects.filter(
        Id_venta=venta
    ).select_related('Id_producto__Catego_Id')
    
    # Calcular totales y estadísticas
    total_items = sum(detalle.Cantidad for detalle in detalles)
    subtotal_sin_iva = venta.Total / Decimal('1.19')  # Asumiendo IVA 19%
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
    """Editar venta - MANTENER SIMPLE"""
    venta = get_object_or_404(Venta, Id_venta=id)
    detalles = Detalle_Venta.objects.filter(Id_venta=venta).select_related('Id_producto')
    
    empleados = User_Empleados.objects.filter(is_active=True, is_staff=True).order_by('first_name')
    productos = producto.objects.filter(Estado='Activo').select_related('Catego_Id').order_by('Nombre')
    
    return render(request, 'templates_ventas/editar_ventas.html', {
        'venta': venta,
        'detalles': detalles,
        'empleados': empleados,
        'productos': productos,
    })