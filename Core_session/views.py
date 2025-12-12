from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from decimal import Decimal
from random import randint

from Empleados.models import User_Empleados
from Membresias.models import Membresia
from Productos.models import producto as Producto
from Categorias.models import categoria as Categoria

from .forms import CambiaContraseñaForm

# ============================
# VISTA DE LOGIN
# ============================
def _parse_date_range(request):
    """Devuelve (fecha_inicio, fecha_fin, str_inicio, str_fin) basados en parámetros GET."""
    fecha_inicio_str = request.GET.get('fecha_inicio', '').strip()
    fecha_fin_str = request.GET.get('fecha_fin', '').strip()

    fecha_inicio = parse_date(fecha_inicio_str) if fecha_inicio_str else None
    fecha_fin = parse_date(fecha_fin_str) if fecha_fin_str else None

    if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
        fecha_inicio, fecha_fin = fecha_fin, fecha_inicio

    return fecha_inicio, fecha_fin, fecha_inicio_str, fecha_fin_str


def login_view(request):
    logout(request)
    # Si ya está autenticado, redirigir
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Usuarios').exists():
            return redirect('Perfil')
        elif request.user.groups.filter(name='Huella').exists():
            return redirect('AsisVista')
        else:
            return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.groups.filter(name='Usuarios').exists():
                return redirect('Perfil')
            elif user.groups.filter(name='Huella').exists():
                return redirect('AsisVista')
            else:
                return redirect('home')
        else:
            if not username:
                messages.error(request, 'Debes ingresar un usuario')
            elif not User_Empleados.objects.filter(username=username).exists():
                messages.error(request, 'Usuario no registrado')
            else:
                messages.error(request, 'Contraseña incorrecta')

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
    
    email = request.session.get('email_recuperacion')
    usuario = User_Empleados.objects.get(email=email)

    if request.method == 'POST':
        form = CambiaContraseñaForm(usuario, request.POST)
        if form.is_valid():
            form.save()
            
            request.session.pop('codigo_recuperacion', None)
            request.session.pop('email_recuperacion', None)
            
            messages.success(request, 'Contraseña actualizada correctamente')
            return redirect('login')
    else:
        form = CambiaContraseñaForm(usuario)
    
    return render(request, 'templates_core_session/contra_nueva.html', {'form': form})


# ============================
# ERRORES / LOGOUT
# ============================

def error_403_view(request, exception=None):
    return render(request, 'templates_errores/403.html', status=403)


def error_404_view(request, exception=None):
    return render(request, 'templates_errores/404.html', status=404)

def error_500_view(request, exception=None):
    return render(request, 'templates_errores/500.html', status=500)


def logout_view(request):
    logout(request)
    return redirect('login')


# ============================
# DASHBOARD (HOME) + CHARTS
# ============================

@login_required(login_url='login')
def home_view(request):
    """Vista principal del dashboard"""
    if request.user.groups.filter(name='Huella').exists():
        messages.error(request, 'No tienes acceso al dashboard')
        return redirect('AsisVista')
    
    hoy = timezone.now().date()
    fecha_limite = hoy + timedelta(days=7)
    fecha_inicio, fecha_fin, fecha_inicio_str, fecha_fin_str = _parse_date_range(request)
    filtro_activo = bool(fecha_inicio or fecha_fin)
    
    membresias_qs = Membresia.objects.filter(Estado='Activo')
    if fecha_inicio:
        membresias_qs = membresias_qs.filter(Fecha_fin__gte=fecha_inicio)
    if fecha_fin:
        membresias_qs = membresias_qs.filter(Fecha_fin__lte=fecha_fin)
    
    if filtro_activo:
        membresias_por_vencer = membresias_qs.count()
    else:
        membresias_por_vencer = Membresia.objects.filter(
            Estado='Activo',
            Fecha_fin__gte=hoy,
            Fecha_fin__lte=fecha_limite
        ).count()
    
    # ================================
    # CARD 1: Usuarios Activos
    # ================================
    usuarios_activos = User_Empleados.objects.filter(is_active=True).count()
    
    # ================================
    # CARD 2: Membresías por Vencer (próximos 7 días)
    # ================================
    membresias_por_vencer = Membresia.objects.filter(
        Estado='Activo',
        Fecha_fin__gte=hoy,
        Fecha_fin__lte=fecha_limite
    ).count()
    
    # ================================
    # CARD 3: Total de Productos Activos
    # ================================
    total_productos = Producto.objects.filter(Estado='Activo').count()
    
    # ================================
    # CARD 4: Stock Bajo (productos con stock < 10)
    # ================================
    stock_bajo = Producto.objects.filter(
        Estado='Activo',
        Stock__lt=10
    ).count()
    
    context = {
        'usuarios_activos': usuarios_activos,
        'membresias_por_vencer': membresias_por_vencer,
        'total_productos': total_productos,
        'stock_bajo': stock_bajo,
        'fecha_inicio': fecha_inicio_str,
        'fecha_fin': fecha_fin_str,
        'filtro_activo': filtro_activo,
    }
    
    return render(request, 'templates_core_session/home.html', context)


@login_required(login_url='login')
def home_chart(request, name):
    """API para gráficos del dashboard"""
    fecha_inicio, fecha_fin, _, _ = _parse_date_range(request)
    
    # ================================
    # GRÁFICO: Productos por Categoría
    # ================================
    if name == 'productos':
        
        # Contar productos activos por categoría
        categorias = Categoria.objects.filter(Estado='Activo')
        
        labels = []
        data = []
        
        for cat in categorias:
            count = Producto.objects.filter(
                Catego_Id=cat,
                Estado='Activo'
            ).count()
            
            if count > 0:
                labels.append(cat.Nombre)
                data.append(count)
        
        # Si no hay datos, placeholder
        if not data:
            labels = ['Sin productos']
            data = [0]
        
        return JsonResponse({
            'labels': labels,
            'data': data,
            'total': sum(data)
        })
    
    # ================================
    # GRÁFICO: Tipos de Membresía
    # ================================
    elif name == 'membresias':
        
        from Tipo_membresia.models import TipoMembresia
        
        tipos = TipoMembresia.objects.filter(Estado='Activo')
        labels = []
        data = []
        
        for tipo in tipos:
            membresias_tipo = Membresia.objects.filter(
                For_Id_tipo_membresia=tipo,
                Estado='Activo'
            )
            if fecha_inicio:
                membresias_tipo = membresias_tipo.filter(Fecha_inicio__date__gte=fecha_inicio)
            if fecha_fin:
                membresias_tipo = membresias_tipo.filter(Fecha_inicio__date__lte=fecha_fin)
            count = membresias_tipo.count()
            
            if count > 0:
                labels.append(tipo.Nombre)
                data.append(count)
        
        # Si no hay datos, placeholder
        if not data:
            labels = ['Sin membresías activas']
            data = [1]
        
        return JsonResponse({
            'labels': labels,
            'data': data,
            'total': sum(data)
        })
    
    return JsonResponse({'error': 'Gráfico no encontrado'}, status=404)
