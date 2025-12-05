from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from decimal import Decimal
from datetime import datetime
from .models import Historial_Ventas


@login_required(login_url='login')
@permission_required('Historial_ventas.view_historial_ventas', login_url='home')
def ListarHistorialVentas(request):
    # Obtener parámetros de filtros
    search_query = request.GET.get('search', '').strip()
    filter_metodo = request.GET.get('metodo', '').strip()
    filter_fecha = request.GET.get('fecha', '').strip()
    page_number = request.GET.get('page', 1)

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

    # Filtro por fecha
    if filter_fecha:
        try:
            fecha_obj = datetime.strptime(filter_fecha, '%Y-%m-%d').date()
            historial = historial.filter(fecha_venta__date=fecha_obj)
        except ValueError:
            pass

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
    hay_filtros = any([search_query, filter_metodo, filter_fecha])

    context = {
        'AllHV': page_obj,
        'total_items': paginator.count,
        'total_ventas': total_ventas,
        'total_recaudado': total_recaudado,
        'search_query': search_query,
        'filter_metodo': filter_metodo,
        'filter_fecha': filter_fecha,
        'hay_filtros': hay_filtros,
    }

    return render(request, 'templates_ventas/historial_ventas.html', context)