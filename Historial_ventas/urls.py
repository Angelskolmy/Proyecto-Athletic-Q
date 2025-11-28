from django.contrib import admin
from django.urls import path,include 
from Historial_ventas import views

urlpatterns = [
    
    path('HistorialVentas/', views.ListarHistorialVentas, name='HistorialVentas')
]  
