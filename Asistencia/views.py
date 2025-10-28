from django.shortcuts import render
from .models import asistencia

def listarAsistencias (request): 

    AllAsis = asistencia.objects.all() 
    Lister = { 'Asistencias' : AllAsis}  
    return render (request, "templates_asistencias/asistencias.html", Lister)
