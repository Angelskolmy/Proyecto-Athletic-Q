from django.shortcuts import render, redirect
from .models import asistencia
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def listarAsistencias (request): 
    #Si NO tiene permiso → redirigir a perfil
    
    if not request.user.has_perm('Asistencia.view_asistencia'):
        messages.warning(request, "No tienes permiso para acceder a esta sección.")
        return redirect('Perfil')  # URL de perfil

    AllAsis = asistencia.objects.all() 
    Lister = { 'Asistencias' : AllAsis}  
    
    return render (request, "templates_asistencias/asistencias.html", Lister)
