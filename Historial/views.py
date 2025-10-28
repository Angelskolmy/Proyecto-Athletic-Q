from django.shortcuts import render
from .models import Historial_usuario

def listHistU(request): 

    ListAllHU= Historial_usuario.objects.all() 
    List={'HistU':ListAllHU} 
    return render (request,'templates_historial_usuario/historial_usuario.html',List)