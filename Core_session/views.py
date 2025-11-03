from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Vista de login
def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        user = authenticate(request, username=correo, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # después de login lo mandamos al dashboard
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')
            return redirect('login')

    return render(request, 'templates_core_session/login2.html')


# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('login')


# Vista del dashboard (protegida)
@login_required(login_url='login')
def home_view(request):
    return render(request, 'templates_core_session/home.html')
