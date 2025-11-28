from django.urls import path
from Tipo_membresia import views

urlpatterns = [
    path('TiposMembresia/', views.listarTiposMembresia, name='TiposMembresia'),
    path('TiposMembresia/crear/', views.crearTipoMembresia, name='CrearTipoMembresia'),
    path('TiposMembresia/editar/<int:Id_tipo_membresia>/', views.editarTipoMembresia, name='EditarTipoMembresia'),
]