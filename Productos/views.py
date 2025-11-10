from django.shortcuts import render, redirect
from .models import producto 
from .models import categoria 
from .forms import ProductoForm 
from django.contrib.auth.decorators import permission_required 
from django.contrib.auth.decorators import login_required


@login_required(login_url='login') 
@permission_required('Productos.view_producto', login_url='login')

def listarProductos (request): 

    AllProd= producto.objects.all()  
    AllCatgo= categoria.objects.all()
    ListProd= {'Productos' : AllProd,
                'Categorias' : AllCatgo} 
    
    return render(request, 'templates_productos/productos.html', ListProd)


def IngresaProductos(request):  

    if request.method == 'POST': 
        Cipher= ProductoForm(request.POST, request.FILES)

        if Cipher.is_valid():
            Cipher.save() 
            return redirect('Producto')        
    else: 
        Cipher= ProductoForm()

    Clave={'Clave' : Cipher} 
    return render (request,'templates_productos/Ingresar_productos.html', Clave)


def EliminarProducto(request, Id_producto):   

    Shigaraki= producto.objects.get(Id_producto=Id_producto) 
    Shigaraki.delete() 
    return redirect ('Producto') 


def DetalleProducto (request, Id_producto): 

    consulta= " SELECT producto.*, categoria.nombre FROM producto join categoria on producto.Catego_Id = categoria.Id_categoria WHERE Id_producto= %s"
    EspecProd= producto.objects.raw(consulta, [Id_producto]) 
    ListEspec= { 'DetalleP' : EspecProd} 
    return render (request, 'templates_productos/Detalle_producto.html' ,ListEspec)