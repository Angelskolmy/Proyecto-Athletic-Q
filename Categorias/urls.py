from django.urls import path
from . import views

urlpatterns = [
    path('Categorias/', views.ListarCategorias, name='Categorias'),
    path('Categorias/crear/', views.CrearCategoria, name='categorias_create'),
    path('Categorias/editar/<int:Id_categoria>/', views.EditarCategoria, name='categorias_edit'),
]