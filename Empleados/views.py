from django.shortcuts import render
from .models import User_Empleados
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
@permission_required('Empleados.view_user_empleados', login_url='home')
def listUsers(request): 

    AllUser= User_Empleados.objects.all() 
    List={'Alluser': AllUser} 
    return render(request,'templates_usuarios/usuarios.html',List)

#@permission_required('Empleados.view_suariogym', login_url='home') este permiso puede hacer todo el view si ese usuario tiene ese permiso

@permission_required('Empleados.usariogym', login_url='login') # este permiso solo sirve para mirar el perfil 
def UsersGym(request): 
    return render(request,'templates_perfil/perfil.html')