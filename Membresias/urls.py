from django.urls import path, include
from . import views

urlpatterns = [
    path('Membresias/', views.ListarMembresias, name='Membresias'),
    path('Membresias/crear/', views.CrearMembresia, name='membresias_create'),
    path('Membresias/editar/<int:id>/', views.EditarMembresia, name='membresias_edit'),
    path('Membresias/detalle/<int:id>/', views.DetalleMembresia, name='membresias_detail'),
]