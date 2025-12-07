from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from decimal import Decimal
from datetime import datetime, time
from django.utils import timezone
from .models import Historial_Ventas


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


@login_required(login_url='login')
@permission_required('Historial_ventas.view_historial_ventas', login_url='home')
def ListarHistorialVentas(request):
    # Obtener parámetros de filtros
    search_query = request.GET.get('search', '').strip()
    filter_metodo = request.GET.get('metodo', '').strip()
    filter_fecha_str = request.GET.get('fecha', '').strip()
    page_number = request.GET.get('page', 1)

    # Parsear fecha
    filter_fecha = _parse_date(filter_fecha_str)

    # Query base con relaciones
    historial = Historial_Ventas.objects.select_related(
        'id_usuario', 
        'id_venta'
    ).order_by('-id_registro')

    # Filtro por búsqueda (nombre, cédula, ID)
    if search_query:
        historial = historial.filter(
            Q(id_usuario__first_name__icontains=search_query) |
            Q(id_usuario__last_name__icontains=search_query) |
            Q(id_usuario__Cedula__icontains=search_query) |
            Q(id_registro__icontains=search_query) |
            Q(id_venta__Id_venta__icontains=search_query)
        )

    # Filtro por método de pago
    if filter_metodo:
        historial = historial.filter(metodo_pago__iexact=filter_metodo)

    # ============================
    # FILTRO POR FECHA
    # ============================
    if filter_fecha:
        start, end = _day_bounds(filter_fecha)
        if start and end:
            historial = historial.filter(fecha_venta__range=(start, end))

    # Calcular estadísticas (sobre los resultados filtrados)
    stats = historial.aggregate(
        total_ventas=Count('id_registro'),
        total_recaudado=Sum('Monto')
    )
    
    total_ventas = stats['total_ventas'] or 0
    total_recaudado = stats['total_recaudado'] or Decimal('0.00')

    # Paginación - 10 registros por página
    paginator = Paginator(historial, 10)
    page_obj = paginator.get_page(page_number)

    # Verificar si hay filtros activos
    hay_filtros = any([search_query, filter_metodo, filter_fecha_str])

    context = {
        'AllHV': page_obj,
        'total_items': paginator.count,
        'total_ventas': total_ventas,
        'total_recaudado': total_recaudado,
        'search_query': search_query,
        'filter_metodo': filter_metodo,
        'filter_fecha': filter_fecha_str,
        'hay_filtros': hay_filtros,
    }

    return render(request, 'templates_ventas/historial_ventas.html', context)