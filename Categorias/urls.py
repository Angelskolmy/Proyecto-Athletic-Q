from django.urls import path, include
from . import views

urlpatterns = [
    path('Categorias/', views.ListarCategorias, name='Categorias'),
    path('Categorias/crear/', views.CrearCategoria, name='categorias_create'),
    path('Categorias/editar/<int:id>/', views.EditarCategoria, name='categorias_edit'),
]