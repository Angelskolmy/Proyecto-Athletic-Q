from django.urls import path
from . import views

urlpatterns = [
    path('Ventas/', views.ListarVentas, name='Ventas'),
    path('Ventas/create/', views.CrearVentas, name='ventas_create'),
    path('Ventas/edit/<int:id>/', views.EditarVentas, name='ventas_edit'),
]