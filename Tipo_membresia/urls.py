from django.urls import path
from Tipo_membresia import views

urlpatterns = [
    path('', views.listarTiposMembresia, name='TiposMembresia'),
    path('crear/', views.crearTipoMembresia, name='CrearTipoMembresia'),
    path('editar/<int:Id_tipo_membresia>/', views.editarTipoMembresia, name='EditarTipoMembresia'),
]