from django.shortcuts import render
from .models import Historial_Ventas


def listHistorialV(request): 

    listHistVent= Historial_Ventas.objects.all() 
    AllHistV= {'AllHV':listHistVent} 
    return render( request, 'templates_historial_ventas\historial_ventas.html' , AllHistV)

