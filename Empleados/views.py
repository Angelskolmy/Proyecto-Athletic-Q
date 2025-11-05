from django.shortcuts import render
from .models import User_Empleados

def listUsers(request): 

    AllUser= User_Empleados.objects.all() 
    List={'Alluser': AllUser} 
    return render(request,'templates_usuarios/usuarios.html',List)

def UsersGym(request): 
    return render(request,'templates_perfil/perfil.html')