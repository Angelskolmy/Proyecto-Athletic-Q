from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Vista de login
def login_view(request):
    logout(request)
    
    if request.method == 'POST':
        usern = request.POST.get('usern')
        password = request.POST.get('password')

        user = authenticate(request, username=usern, password=password)

        if user is not None:
            login(request, user)
            
            if user.groups.filter(name='Usuarios').exists():
                return redirect('Perfil')
            
            return redirect('home')  # después de login lo mandamos al dashboard
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return redirect('login')

    return render(request, 'templates_core_session/login2.html')
# Vista para recuperar
def recuperar_view(request):
    return render(request, 'templates_core_session/recuperar2.html')

def codigo_view(request):
    return render(request, 'templates_core_session/codigo_recup2.html')

def nueva_view(request):
    return render(request, 'templates_core_session/nuevo2.html')

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('login')

# Vista del dashboard (protegida)
@login_required(login_url='login')
def home_view(request):
    return render(request, 'templates_core_session/home.html')
