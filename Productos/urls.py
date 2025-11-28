from django.contrib import admin
from django.urls import path,include 
from Productos import views

urlpatterns = [
    path('Producto/', views.listarProductos, name='Producto'), 
    path('IngresoProd/', views.IngresaProductos, name='IngresoProd'), 
    path('DelProd/<int:Id_producto>/', views.EliminarProducto, name='DelProd'), 
    path('SpecProd/<int:Id_producto>/', views.DetalleProducto, name='SpecProd'), 
    path('EditProd/<int:Id_producto>/', views.Editar_Producto, name='EditProd'), 
    path('BusquedaP/', views.busqueda_producto, name='BusquedaP'), 
    path('ProdRes/', views.excel_content, name='ProdRes'),
]  