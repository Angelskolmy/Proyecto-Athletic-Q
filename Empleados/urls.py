from django.urls import path
from . import views

urlpatterns = [
    # Listado / CRUD básico
    path('Empleados/', views.ListarEmpleados, name='Empleados'),
    path('Empleados/crear/', views.CrearEmpleado, name='empleados_create'),
    path('Empleados/editar/<int:id>/', views.EditarEmpleado, name='empleados_edit'),
    path('Empleados/detalle/<int:id>/', views.DetalleEmpleado, name='empleados_detail'),

    # Perfil del usuario autenticado (CLIENTE)
    path('Usuario_Gym/', views.UsersGym, name='Perfil'),
    
    # Cambiar contraseña del cliente
    path('Usuario_Gym/cambiar-password/', views.CambiarPasswordCliente, name='cambiar_password_cliente'),
    
    # Detalle de rutina
    path('Usuario_Gym/rutina/<int:id>/', views.DetalleRutina, name='detalle_rutina'),
    
    # Perfil admin y empleados
    path('mi-perfil/', views.MiPerfil, name='mi_perfil'),

    # Captura 
    path('Empleados/<int:empleado_id>/capturar-huella/', views.capturar_huella, name='capturar_huella'),

    # Guardarhuellas
    path('Empleados/guardar-huellas/', views.guardar_huellas, name='guardar_huellas'),
    
    # validar huella
    path("Empleados/validar-huella/", views.validar_huella, name="validar_huella"),
]