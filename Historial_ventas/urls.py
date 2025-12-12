from django.contrib import admin
from django.urls import path,include 
from Historial_ventas import views

urlpatterns = [
    path('HistorialVentas/', views.ListarHistorialVentas, name='HistorialVentas'),
    path('HistorialVentas/exportar/excel/', views.exportar_historial_ventas_excel, name='historial_ventas_export_excel'),
    path('HistorialVentas/exportar/pdf/', views.exportar_historial_ventas_pdf, name='historial_ventas_export_pdf'),
]
