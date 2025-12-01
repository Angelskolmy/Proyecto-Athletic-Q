from django.contrib import admin
from django.urls import path,include 
from Asistencia import views

urlpatterns = [
    
    path('AsisVistas/', views.verPerfilasistencias , name='AsisVista'),
    path('Asistencias/', views.listarAsistencias, name='Asistencias'),
]  
        