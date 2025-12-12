from django.contrib import admin
from django.urls import path,include 
from Asistencia import views

urlpatterns = [
    
    path('AsisVistas/', views.verPerfilasistencias , name='AsisVista'),
    path('Asistencias/', views.listarAsistencias, name='Asistencias'),
    path('Asistencias/exportar/excel/', views.exportar_asistencias_excel, name='asistencias_exportar_excel'),
    path('Asistencias/exportar/pdf/', views.exportar_asistencias_pdf, name='asistencias_exportar_pdf'),
] 
