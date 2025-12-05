from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from random import randint

from Empleados.models import User_Empleados
from Membresias.models import Membresia
from Productos.models import producto as Producto
from Asistencia.models import Asistencia

from .forms import CambiaContraseñaForm

# ============================
# VISTA DE LOGIN
# ============================
def login_view(request):
    # Cerrar cualquier sesión previa
    logout(request)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirigir según el grupo
            if user.groups.filter(name='Usuarios').exists():
                return redirect('Perfil')
            elif user.groups.filter(name='Huella').exists():
                return redirect('AsisVista')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'templates_core_session/login.html')


# ============================
# RECUPERACIÓN DE CONTRASEÑA
# ============================

def enviar_codigo(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        try:
            usuario = User_Empleados.objects.get(email=email)
            codigo = randint(100000, 999999)
            
            request.session['codigo_recuperacion'] = codigo
            request.session['email_recuperacion'] = email
            
            send_mail(
                'Código de recuperación - Athletic-Q',
                f'Tu código de recuperación es: {codigo}',
                'noreply@athletic-q.com',
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Código enviado a tu correo')
            return redirect('codigo_recuperacion')
            
        except User_Empleados.DoesNotExist:
            messages.error(request, 'No existe una cuenta con ese correo')

    return render(request, 'templates_core_session/correo.html')


def vista_codigo(request):
    if 'email_recuperacion' not in request.session:
        return redirect('correo')
    return render(request, 'templates_core_session/codigo_recup.html')


def validar_codigo(request):
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo', '')
        codigo_guardado = request.session.get('codigo_recuperacion')
        
        if str(codigo_ingresado) == str(codigo_guardado):
            return redirect('contra_nueva')
        else:
            messages.error(request, 'Código incorrecto')
            return redirect('codigo_recuperacion')
    
    return redirect('codigo_recuperacion')


def invalidar_codigo(request):
    request.session.pop('codigo_recuperacion', None)
    request.session.pop('email_recuperacion', None)
    return redirect('correo')


def reenviar_codigo(request):
    email = request.session.get('email_recuperacion')
    if email:
        codigo = randint(100000, 999999)
        request.session['codigo_recuperacion'] = codigo
        
        send_mail(
            'Nuevo código de recuperación - Athletic-Q',
            f'Tu nuevo código de recuperación es: {codigo}',
            'noreply@athletic-q.com',
            [email],
            fail_silently=False,
        )
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})


def vista_cambiar_contraseña(request):
    if 'email_recuperacion' not in request.session:
        return redirect('correo')
    
    if request.method == 'POST':
        form = CambiaContraseñaForm(request.POST)
        if form.is_valid():
            email = request.session.get('email_recuperacion')
            nueva_password = form.cleaned_data['password1']
            
            usuario = User_Empleados.objects.get(email=email)
            usuario.set_password(nueva_password)
            usuario.save()
            
            request.session.pop('codigo_recuperacion', None)
            request.session.pop('email_recuperacion', None)
            
            messages.success(request, 'Contraseña actualizada correctamente')
            return redirect('login')
    else:
        form = CambiaContraseñaForm()
    
    return render(request, 'templates_core_session/contra_nueva.html', {'form': form})


# ============================
# ERRORES / LOGOUT
# ============================

def error_403_view(request, exception=None):
    return render(request, 'errors/403.html', status=403)


def error_404_view(request, exception=None):
    return render(request, 'errors/404.html', status=404)


def logout_view(request):
    logout(request)
    return redirect('login')


# ============================
# DASHBOARD (HOME) + CHARTS
# ============================

@login_required(login_url='login')
def home_view(request):
    """Vista principal del dashboard con estadísticas"""
    
    hoy = timezone.now().date()
    
    # ========================================
    # CARD 1: USUARIOS ACTIVOS
    # ========================================
    usuarios_activos = User_Empleados.objects.filter(is_active=True).count()
    
    # ========================================
    # CARD 2: MEMBRESÍAS POR VENCER (próximos 7 días)
    # ========================================
    fecha_limite = hoy + timedelta(days=7)
    membresias_por_vencer = Membresia.objects.filter(
        Estado='Activo',
        Fecha_fin__gte=hoy,
        Fecha_fin__lte=fecha_limite
    ).count()
    
    # ========================================
    # CARD 3: ASISTENCIAS DEL MES
    # ========================================
    primer_dia_mes = hoy.replace(day=1)
    asistencias_mes = Asistencia.objects.filter(
        fecha_entrada__date__gte=primer_dia_mes,
        fecha_entrada__date__lte=hoy
    ).count()
    
    # ========================================
    # CARD 4: PRODUCTOS CON STOCK BAJO (menos de 10)
    # ========================================
    stock_bajo = Producto.objects.filter(
        Estado='Activo',
        Stock__lt=10
    ).count()
    
    # ========================================
    # ASISTENCIAS DE HOY
    # ========================================
    asistencias_hoy = Asistencia.objects.filter(
        fecha_entrada__date=hoy
    ).count()
    
    context = {
        'usuarios_activos': usuarios_activos,
        'membresias_por_vencer': membresias_por_vencer,
        'asistencias_mes': asistencias_mes,
        'asistencias_hoy': asistencias_hoy,
        'stock_bajo': stock_bajo,
    }
    
    return render(request, 'templates_core_session/home.html', context)


@login_required(login_url='login')
def home_chart(request, name):
    """
    API para obtener datos de gráficos vía AJAX
    name puede ser: 'asistencias' o 'membresias'
    """
    
    hoy = timezone.now().date()
    
    # ========================================
    # GRÁFICO DE ASISTENCIAS (últimos 7 días)
    # ========================================
    if name == 'asistencias':
        
        fecha_inicio = hoy - timedelta(days=6)
        fecha_fin = hoy
        
        # Consultar asistencias agrupadas por día
        asistencias = Asistencia.objects.filter(
            fecha_entrada__date__gte=fecha_inicio,
            fecha_entrada__date__lte=fecha_fin
        ).annotate(
            dia=TruncDay('fecha_entrada')
        ).values('dia').annotate(
            total=Count('id')
        ).order_by('dia')
        
        # Crear diccionario con los datos
        asistencias_dict = {}
        for a in asistencias:
            if a['dia']:
                asistencias_dict[a['dia'].date()] = a['total']
        
        # Llenar todos los días del rango
        labels = []
        data = []
        dias_semana = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        
        current = fecha_inicio
        while current <= fecha_fin:
            dia_nombre = dias_semana[current.weekday()]
            labels.append(f"{dia_nombre} {current.day}")
            data.append(asistencias_dict.get(current, 0))
            current += timedelta(days=1)
        
        return JsonResponse({
            'labels': labels,
            'data': data,
            'total': sum(data)
        })
    
    # ========================================
    # GRÁFICO DE MEMBRESÍAS (por tipo)
    # ========================================
    elif name == 'membresias':
        
        # Contar membresías activas por tipo
        membresias = Membresia.objects.filter(
            Estado='Activo'
        ).values(
            'For_Id_tipo_membresia__Nombre'
        ).annotate(
            cantidad=Count('Id_membresia')
        ).order_by('-cantidad')
        
        labels = [m['For_Id_tipo_membresia__Nombre'] or 'Sin tipo' for m in membresias]
        data = [m['cantidad'] for m in membresias]
        
        return JsonResponse({
            'labels': labels,
            'data': data,
            'total': sum(data)
        })
    
    # ========================================
    # GRÁFICO DE USUARIOS POR ROL
    # ========================================
    elif name == 'usuarios':
        
        from django.contrib.auth.models import Group
        
        usuarios_por_grupo = []
        grupos = Group.objects.all()
        
        for grupo in grupos:
            count = User_Empleados.objects.filter(groups=grupo, is_active=True).count()
            if count > 0:
                usuarios_por_grupo.append({
                    'nombre': grupo.name,
                    'cantidad': count
                })
        
        # Ordenar por cantidad
        usuarios_por_grupo.sort(key=lambda x: x['cantidad'], reverse=True)
        
        labels = [u['nombre'] for u in usuarios_por_grupo]
        data = [u['cantidad'] for u in usuarios_por_grupo]
        
        return JsonResponse({
            'labels': labels,
            'data': data,
            'total': sum(data)
        })
    
    return JsonResponse({'error': 'Gráfico no encontrado'}, status=404)