from decimal import Decimal, InvalidOperation
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.apps import apps

# modelos
from .models import Venta
from Detalle_venta.models import Detalle_Venta
from Productos.models import producto
from Empleados.models import User_Empleados
from Categorias.models import categoria

@transaction.atomic
def ListarVentas(request):
    AllVents = Venta.objects.select_related('id_usuario').all().order_by('-Fecha')
    print("Ventas encontradas:", AllVents.count())  # Debug
    return render(request, "templates_ventas/ventas.html", {'Ventas': AllVents})

@transaction.atomic 
def CrearVentas(request):
    if request.method == 'POST':
        try:
            # Crear la venta principal
            venta = Venta.objects.create(
                id_usuario_id=request.POST.get('empleado_id'),
                Total=request.POST.get('total')
            )
            
            # Crear los detalles de venta
            productos = request.POST.getlist('producto_id[]')
            cantidades = request.POST.getlist('cantidad[]')
            precios = request.POST.getlist('precio[]')
            subtotales = request.POST.getlist('subtotal[]')
            
            for i in range(len(productos)):
                Detalle_Venta.objects.create(
                    Id_venta=venta,
                    Id_producto_id=productos[i],
                    Tipo_Pago=request.POST.get('metodo_pago'),
                    Cantidad=cantidades[i],
                    Subtotal=subtotales[i],
                    Total=request.POST.get('total')
                )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Venta creada correctamente',
                'redirect': '/Ventas/'
            })
            
        except Exception as e:
            print(f"Error al crear venta: {str(e)}")  # Debug
            return JsonResponse({
                'status': 'error',
                'message': f'Error al crear la venta: {str(e)}'
            }, status=400)

    # Si es GET, mostrar formulario
    cliente_group_names = ['Clientes', 'clientes', 'Cliente', 'cliente']
    empleado_group_names = ['Empleados', 'empleados', 'Empleado', 'empleado']

    clientes = User_Empleados.objects.filter(groups__name__in=cliente_group_names).distinct()
    if not clientes.exists():
        clientes = User_Empleados.objects.all()

    empleados = User_Empleados.objects.filter(groups__name__in=empleado_group_names).distinct()
    if not empleados.exists():
        empleados = User_Empleados.objects.filter(is_staff=True) or User_Empleados.objects.all()

    productos = producto.objects.all()
    categorias = categoria.objects.filter(Estado='Activo').order_by('Nombre')

    return render(request, 'templates_ventas/crear_ventas.html', {
        'clientes': clientes,
        'empleados': empleados,
        'productos': productos,
        'categorias': categorias,
        'now': timezone.now(),
    })

@transaction.atomic
def EditarVentas(request, id):
    venta = get_object_or_404(Venta, pk=id)
    detalles = Detalle_Venta.objects.filter(Id_venta=venta).select_related('Id_producto')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Actualizar venta principal
                venta.id_usuario_id = request.POST.get('empleado_id')
                venta.Total = request.POST.get('total')
                venta.save()

                # Eliminar detalles antiguos
                Detalle_Venta.objects.filter(Id_venta=venta).delete()

                # Crear nuevos detalles
                productos = request.POST.getlist('producto_id[]')
                cantidades = request.POST.getlist('cantidad[]')
                precios = request.POST.getlist('precio[]')
                subtotales = request.POST.getlist('subtotal[]')

                for i in range(len(productos)):
                    Detalle_Venta.objects.create(
                        Id_venta=venta,
                        Id_producto_id=productos[i],
                        Tipo_Pago=request.POST.get('metodo_pago'),
                        Cantidad=cantidades[i],
                        Subtotal=subtotales[i],
                        Total=request.POST.get('total')
                    )

                return JsonResponse({
                    'status': 'success',
                    'message': 'Venta actualizada correctamente',
                    'redirect': '/Ventas/'
                })

        except Exception as e:
            print(f"Error al actualizar venta: {str(e)}")  # Debug
            return JsonResponse({
                'status': 'error',
                'message': f'Error al actualizar la venta: {str(e)}'
            }, status=400)

    # Si es GET, mostrar formulario de edición
    cliente_group_names = ['Clientes', 'clientes', 'Cliente', 'cliente']
    empleado_group_names = ['Empleados', 'empleados', 'Empleado', 'empleado']

    clientes = User_Empleados.objects.filter(groups__name__in=cliente_group_names).distinct()
    if not clientes.exists():
        clientes = User_Empleados.objects.all()

    empleados = User_Empleados.objects.filter(groups__name__in=empleado_group_names).distinct()
    if not empleados.exists():
        empleados = User_Empleados.objects.filter(is_staff=True) or User_Empleados.objects.all()

    productos = producto.objects.all()
    categorias = categoria.objects.filter(Estado='Activo').order_by('Nombre')

    return render(request, 'templates_ventas/editar_ventas.html', {
        'venta': venta,
        'detalles': detalles,
        'clientes': clientes,
        'empleados': empleados,
        'productos': productos,
        'categorias': categorias,
        'now': timezone.now(),
    })