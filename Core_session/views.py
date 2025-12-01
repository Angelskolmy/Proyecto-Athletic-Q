from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from Empleados.models import User_Empleados
from random import randint
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import CambiaContraseñaForm
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
            
            if user.groups.filter(name='Huella').exists():
                return redirect('AsisVista')
            
            return redirect('home')  # después de login lo mandamos al dashboard
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return redirect('login')

    return render(request, 'templates_core_session/login.html')

# funcion de para el envio de codigo 
def enviar_codigo(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            usuario = User_Empleados.objects.get(email=email)

            codigo = randint(100000, 999999)

            request.session['codigo'] = codigo
            request.session['email'] = email

            send_mail(
                'Recuperación de contraseña',
                f'Tu código de recuperación es: {codigo}',
                'smorales.joan@gmail.com',
                [email],
                fail_silently=False,
            )

            # Activar reset del contador SOLO una vez
            request.session["contador_reset"] = True

            return redirect("codigo_recuperacion")  # ⬅ CAMBIO IMPORTANTE

        except User_Empleados.DoesNotExist:
            messages.error(request, 'No existe un usuario con ese correo registrado')
            return render(request, 'templates_core_session/correo.html')

    return render(request, 'templates_core_session/correo.html')

# vista para ingresar el codigo 
def vista_codigo(request):
    #🚫 Si no hay email guardado → volver a ingresar email
    if "email" not in request.session:
        return redirect("correo")
    
    # limpiar bandera de reinicio si existe
    request.session.pop("contador_reset", None)

    bandera = request.session.get("contador_reset", False)

    response = render(request, "templates_core_session/codigo_recup.html", {
        "contador_reset": bandera
    })

    if "contador_reset" in request.session:
        del request.session["contador_reset"]

    return response

# funcion para validar codigo 
def validar_codigo(request):
    #🚫 Si no hay email guardado → volver a ingresar email
    if "email" not in request.session:
        return redirect("correo")
    
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo', '')

        # 1. Verificar si está vacío
        if not codigo_ingresado.strip():
            messages.error(request, "Debes ingresar el código.")
            return redirect('codigo')  # O renderizar nuevamente el template

        # 2. Verificar que sea un número
        if not codigo_ingresado.isdigit():
            messages.error(request, "El código debe ser numérico.")
            return redirect('codigo')

        # 3. Convertir a entero SI ya es seguro hacerlo
        codigo_ingresado = int(codigo_ingresado)

        codigo_sesion = request.session.get('codigo')
        
        if str(codigo_ingresado) == str(codigo_sesion):
            # Invalidar código porque ya fue usado
            
            
            request.session["codigo_valido"] = True
            
            del request.session["codigo"]
            
            return redirect("contra_nueva")
        else:
            messages.error(request, "El código ingresado es incorrecto.")
            return redirect('codigo')
        
    return render(request, 'templates_core_session/codigo_recup.html')

# funcion para invalidar codigo 
def invalidar_codigo(request):
    #🚫 Si no hay email guardado → volver a ingresar email
    if "email" not in request.session:
        return redirect("correo")
    
    request.session['codigo'] = None
    return JsonResponse({'status': 'ok'})

# funcion para reenviar  codigo 
def reenviar_codigo(request):
    #🚫 Si no hay email guardado → volver a ingresar email
    if "email" not in request.session:
        return redirect("correo")
    
    email = request.session.get('email')

    if not email:
        return JsonResponse({'error': 'No hay email en sesión'}, status=400)

    # Generar nuevo código
    import random
    codigo = random.randint(100000, 999999)

    request.session['codigo'] = codigo

    # Enviar correo
    send_mail(
                'Tu nuevo código',
                f'Tu nuevo código es: {codigo}',
                'smorales.joan@gmail.com',
                [email],
                fail_silently=False,
            )

    return JsonResponse({'status': 'ok'})


# vista para cambiar contraseña
def vista_cambiar_contraseña(request):
    #🚫 Si no hay email guardado → volver a ingresar email
    if "email" not in request.session:
        return redirect("correo")
    
    if not request.session.get("codigo_valido"):
        
        return redirect("codigo_recuperacion")
    
    request.session["codigo_valido"] = None
    
    
    email = request.session.get('email')
    usuario = User_Empleados.objects.get(email=email)

    if request.method == 'POST':
        form = CambiaContraseñaForm(usuario, request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CambiaContraseñaForm(usuario)

    return render(request, 'templates_core_session/contra_nueva.html', {'form': form})
    
# error de permisos
def error_403_view(request, exception=None):
    # Si NO está autenticado → login
    if not request.user.is_authenticated:
        return redirect('login')

    # Si está autenticado pero sin permisos → mostrar página 403
    return render(request, 'templates_errores/403.html', status=403)

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('login')

# Vista del dashboard (protegida)
@login_required(login_url='login')
def home_view(request):

    user = request.user

    # ADMIN → Admin dashboard
    if user.is_superuser:
        return render(request, 'templates_core_session/home.html')
    
    if user.groups.filter(name='Admin').exists():
        return render(request, 'templates_core_session/home.html')
    
    # INSPECTOR → su página
    if user.groups.filter(name='Inspector').exists():
        return render(request, 'templates_core_session/home.html')

    # EMPLEADO → su página
    if user.groups.filter(name='Empleados').exists():
        return render(request, 'templates_core_session/home.html')

    # USUARIO NORMAL → Perfil
    return redirect('Perfil')