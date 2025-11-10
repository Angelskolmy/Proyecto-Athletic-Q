from django.shortcuts import render
from .models import Historial_Ventas
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
@permission_required('Historial_ventas.view_historial_ventas', login_url='home')

def listHistorialV(request): 

    listHistVent= Historial_Ventas.objects.all() 
    AllHistV= {'AllHV':listHistVent} 
    return render( request, 'templates_historial_ventas\historial_ventas.html' , AllHistV)

