from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import producto 
from .models import categoria 
from .forms import ProductoForm 
from django.contrib.auth.decorators import permission_required 
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='login') 
@permission_required('Productos.view_producto', login_url='login')
def listarProductos (request): 
    AllProd= producto.objects.all()  
    AllCatgo= categoria.objects.all()
    ListProd= {'Productos' : AllProd,
                'Categorias' : AllCatgo} 
    
    return render(request, 'templates_productos/productos.html', ListProd)


@login_required(login_url='login')
@permission_required('Productos.add_producto', login_url='Producto')
def IngresaProductos(request):  
    if request.method == 'POST': 
        Cipher= ProductoForm(request.POST, request.FILES)

        if Cipher.is_valid():
            Cipher.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('Producto')        
    else: 
        Cipher= ProductoForm()

    Clave={'Clave' : Cipher} 
    return render (request,'templates_productos/Ingresar_productos.html', Clave)

@login_required(login_url='login')
@permission_required('Productos.view_producto', login_url='Producto')
def DetalleProducto (request, Id_producto): 
    consulta= "SELECT producto.*, categoria.nombre FROM producto join categoria on producto.Catego_Id = categoria.Id_categoria WHERE Id_producto= %s"
    EspecProd= producto.objects.raw(consulta, [Id_producto]) 
    ListEspec= { 'DetalleP' : EspecProd} 
    return render (request, 'templates_productos/Detalle_producto.html' ,ListEspec)


# funcion para actualizar stock
@require_http_methods(["POST"])
def ActualizarStock(request, Id_producto):
    try:
        prod = get_object_or_404(producto, Id_producto=Id_producto)
        nuevo_stock = request.POST.get('stock')
        
        if nuevo_stock is None:
            return JsonResponse({
                'success': False,
                'message': 'Stock no proporcionado'
            }, status=400)
        
        try:
            nuevo_stock = int(nuevo_stock)
            if nuevo_stock < 0:
                return JsonResponse({
                    'success': False,
                    'message': 'El stock no puede ser negativo'
                }, status=400)
        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'Stock inválido'
            }, status=400)
        
        stock_anterior = prod.Stock
        prod.Stock = nuevo_stock
        prod.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Stock actualizado de {stock_anterior} a {nuevo_stock}',
            'nuevo_stock': nuevo_stock
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al actualizar: {str(e)}'
        }, status=500)