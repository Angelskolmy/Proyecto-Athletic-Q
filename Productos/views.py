from django.shortcuts import render
from .models import producto 
from .models import categoria

def listarProductos (request): 

    AllProd= producto.objects.all()  
    AllCatgo= categoria.objects.all()
    ListProd= {'Productos' : AllProd,
                'Categorias' : AllCatgo} 
    
    return render(request, 'templates_productos/productos.html', ListProd)


