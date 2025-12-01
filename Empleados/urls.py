from django.urls import path
from . import views

urlpatterns = [
    # Listado / CRUD básico
    path('Empleados/', views.ListarEmpleados, name='Empleados'),
    path('Empleados/crear/', views.CrearEmpleado, name='empleados_create'),
    path('Empleados/editar/<int:id>/', views.EditarEmpleado, name='empleados_edit'),

    # Perfil del usuario autenticado
    path('Usuario_Gym/', views.UsersGym, name='Perfil'),
    
    #Perfil admin y empleados
    path('mi-perfil/', views.MiPerfil, name='mi_perfil'),

    # Captura y guardado de huella
    path('Empleados/<int:empleado_id>/capturar-huella/', views.capturar_huella, name='capturar_huella'),
]