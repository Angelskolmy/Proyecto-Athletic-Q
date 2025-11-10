from django.shortcuts import render
from .models import Historial_usuario
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
@permission_required('Historial.view_historial_usuario', login_url='home')
def listHistU(request): 

    ListAllHU= Historial_usuario.objects.all() 
    List={'HistU':ListAllHU} 
    return render (request,'templates_historial_usuario/historial_usuario.html',List)