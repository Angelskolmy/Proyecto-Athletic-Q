from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, time
from django.utils import timezone
from .models import Asistencia
from .forms import AsistenciaForm


@permission_required('Asistencia.view_asistencia', raise_exception=True)
def verPerfilasistencias(request):
    user = request.user
    if user.groups.filter(name='Admin').exists():
        return redirect('Asistencias')
    if user.groups.filter(name='Huella').exists():
        return render(request, "templates_asistencias/asistencias_huella.html")
    return redirect('Perfil')


def _parse_date(value: str):
    """Convierte 'YYYY-MM-DD' en date, o None si viene vacío/mal."""
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _day_bounds(date_obj):
    """
    Devuelve (inicio_de_día, fin_de_día) como datetimes *aware* si hay timezone.
    Ej: 2025-12-03 -> (2025-12-03 00:00, 2025-12-03 23:59:59.999999)
    """
    if not date_obj:
        return None, None

    start = datetime.combine(date_obj, time.min)
    end = datetime.combine(date_obj, time.max)

    # Si usas USE_TZ = True, hacemos los datetimes aware
    if timezone.is_naive(start):
        start = timezone.make_aware(start)
        end = timezone.make_aware(end)

    return start, end


@permission_required('Asistencia.view_asistencia', raise_exception=True)
def listarAsistencias(request):
    # Obtener parámetros de filtros
    nombre_query = request.GET.get('nombre', '').strip()
    tipo_usuario = request.GET.get('tipo', '').strip()
    fecha_entrada_str = request.GET.get('fecha_entrada', '').strip()
    fecha_salida_str = request.GET.get('fecha_salida', '').strip()
    page_number = request.GET.get('page', 1)

    # Debug (puedes quitarlos luego)
    print("GET:", request.GET)
    print("fecha_entrada_str:", repr(fecha_entrada_str))
    print("fecha_salida_str:", repr(fecha_salida_str))

    # Parsear strings a date
    fecha_entrada = _parse_date(fecha_entrada_str)
    fecha_salida = _parse_date(fecha_salida_str)

    # Query base ordenada por ID ascendente
    asistencias = Asistencia.objects.select_related('id_usuario').order_by('id')

    # Filtro por nombre
    if nombre_query:
        asistencias = asistencias.filter(
            Q(id_usuario__first_name__icontains=nombre_query) |
            Q(id_usuario__last_name__icontains=nombre_query) |
            Q(id_usuario__username__icontains=nombre_query) |
            Q(id_usuario__Cedula__icontains=nombre_query)
        )

    # Filtro por tipo de usuario (rol)
    if tipo_usuario:
        if tipo_usuario.lower() == 'admin':
            asistencias = asistencias.filter(
                Q(rol__iexact='Admin') |
                Q(rol__iexact='Administrador') |
                Q(rol__icontains='admin')
            )
        elif tipo_usuario.lower() == 'empleado':
            asistencias = asistencias.filter(
                Q(rol__iexact='Empleado') |
                Q(rol__iexact='Empleados') |
                Q(rol__icontains='empleado')
            )
        elif tipo_usuario.lower() == 'cliente':
            asistencias = asistencias.filter(
                Q(rol__iexact='Cliente') |
                Q(rol__iexact='Usuario') |
                Q(rol__iexact='Usuarios') |
                Q(rol__icontains='cliente') |
                Q(rol__icontains='usuario')
            )
        elif tipo_usuario.lower() == 'entrenador':
            asistencias = asistencias.filter(
                Q(rol__iexact='Entrenador') |
                Q(rol__icontains='entrenador')
            )
        else:
            asistencias = asistencias.filter(rol__icontains=tipo_usuario)

    # ============================
    # FILTRO POR FECHAS (ENTRADA O SALIDA EN EL RANGO)
    # ============================

    # Caso 1: solo fecha de entrada (un día)
    if fecha_entrada and not fecha_salida:
        start, end = _day_bounds(fecha_entrada)
        asistencias = asistencias.filter(
            Q(fecha_entrada__range=(start, end)) |
            Q(fecha_salida__range=(start, end))
        )

    # Caso 2: solo fecha de salida (un día)
    elif fecha_salida and not fecha_entrada:
        start, end = _day_bounds(fecha_salida)
        asistencias = asistencias.filter(
            Q(fecha_entrada__range=(start, end)) |
            Q(fecha_salida__range=(start, end))
        )

    # Caso 3: ambas fechas → rango completo
    elif fecha_entrada and fecha_salida:
        # Corregir si vienen al revés
        if fecha_entrada > fecha_salida:
            fecha_entrada, fecha_salida = fecha_salida, fecha_entrada

        start, _ = _day_bounds(fecha_entrada)
        _, end = _day_bounds(fecha_salida)

        # Entradas o salidas que caigan en cualquier momento
        # entre start y end
        asistencias = asistencias.filter(
            Q(fecha_entrada__range=(start, end)) |
            Q(fecha_salida__range=(start, end))
        )

    # PROCESAR CADA ASISTENCIA PARA AGREGAR INFO
    asistencias_lista = list(asistencias)
    for asistencia in asistencias_lista:
        cumplio_horario = None
        horas_trabajadas = None
        
        if asistencia.fecha_salida and asistencia.fecha_entrada:
            diferencia = asistencia.fecha_salida - asistencia.fecha_entrada
            horas_trabajadas = diferencia.total_seconds() / 3600
            cumplio_horario = horas_trabajadas >= 6
        
        asistencia.cumplio_horario = cumplio_horario
        asistencia.horas_trabajadas = round(horas_trabajadas, 2) if horas_trabajadas else None

    # Paginación - 15 registros por página
    paginator = Paginator(asistencias_lista, 15)
    page_obj = paginator.get_page(page_number)

    # Verificar si hay filtros activos
    hay_filtros = any([nombre_query, tipo_usuario, fecha_entrada_str, fecha_salida_str])

    context = {
        "Asistencias": page_obj,
        "total_items": paginator.count,
        "nombre_query": nombre_query,
        "tipo_usuario": tipo_usuario,
        "fecha_entrada": fecha_entrada_str,
        "fecha_salida": fecha_salida_str,
        "hay_filtros": hay_filtros,
    }
    
    return render(request, "templates_asistencias/asistencias.html", context)
