from django.shortcuts import render
from .models import producto 
from .models import categoria
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
@permission_required('Productos.view_producto', login_url='GYM')
def listarProductos (request): 

    AllProd= producto.objects.all()  
    AllCatgo= categoria.objects.all()
    ListProd= {'Productos' : AllProd,
                'Categorias' : AllCatgo} 
    
    return render(request, 'templates_productos/productos.html', ListProd)


