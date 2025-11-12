from django.contrib import admin
from django.urls import path,include 
from Productos import views

urlpatterns = [
    path('Producto/', views.listarProductos, name='Producto'), 
    path('IngresoProd/', views.IngresaProductos, name='IngresoProd'), 
    path('SpecProd/<int:Id_producto>/', views.DetalleProducto, name='SpecProd'),
    path('ActualizarStock/<int:Id_producto>/', views.ActualizarStock, name='ActualizarStock'),
]