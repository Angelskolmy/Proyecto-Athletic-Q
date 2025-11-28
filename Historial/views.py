from django.shortcuts import render, redirect
from .models import Historial_usuario
from django.contrib.auth.decorators import permission_required 
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator  
from urllib.parse import urlencode

def listHistU(request): 

    ListAllHU= Historial_usuario.objects.all() 
    List={'HistU':ListAllHU} 
    return render (request,'templates_historial_usuario/historial_usuario.html',List)