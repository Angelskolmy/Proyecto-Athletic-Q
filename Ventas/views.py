from django.shortcuts import render
from .models import Venta 
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
@permission_required('Ventas.view_venta', login_url='home')
def ListarVentas(request): 

    AllVents= Venta.objects.all() 
    ContentV= {'Ventas': AllVents} 
    return render (request, "templates_ventas/ventas.html", ContentV)

