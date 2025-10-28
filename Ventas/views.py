from django.shortcuts import render
from .models import Venta 

def ListarVentas(request): 

    AllVents= Venta.objects.all() 
    ContentV= {'Ventas': AllVents} 
    return render (request, "templates_ventas/ventas.html", ContentV)

