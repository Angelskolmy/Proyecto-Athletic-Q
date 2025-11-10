from django.urls import path, include
from . import views

urlpatterns = [
    path('Empleados/', views.ListarEmpleados, name='Empleados'),
    path('Usuario_Gym/',views.UsersGym, name='Perfil'),
    path('Empleados/crear/', views.CrearEmpleado, name='empleados_create'),
    path('Empleados/editar/<int:id>/', views.EditarEmpleado, name='empleados_edit'),
    path('Empleados/registrar-huella/<int:user_id>/', views.RegistrarHuella, name='registrar_huella'),
]