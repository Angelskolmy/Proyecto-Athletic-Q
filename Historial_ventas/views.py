from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.contrib.auth.decorators import permission_required, login_required
from .models import Historial_Ventas

@login_required(login_url='login')
@permission_required('Historial_ventas.view_historial_ventas', login_url='home')
def ListarHistorialVentas(request):
    # Parámetros de búsqueda y filtrado
    search_query = request.GET.get('search', '').strip()
    filter_metodo = request.GET.get('metodo', '')
    filter_fecha = request.GET.get('fecha', '')
    page_number = request.GET.get('page', 1)
    items_per_page = int(request.GET.get('items_per_page', 10))
    
    # Consulta base con optimización
    historial = Historial_Ventas.objects.select_related('id_usuario').all().order_by('-fecha_venta')
    
    # Aplicar búsqueda
    if search_query:
        search_filters = Q(id_usuario__first_name__icontains=search_query) | \
                        Q(id_usuario__last_name__icontains=search_query) | \
                        Q(id_usuario__Cedula__icontains=search_query)
        
        if search_query.isdigit():
            search_filters |= Q(id_registro=int(search_query))
        
        historial = historial.filter(search_filters)
    
    # Filtrar por método de pago
    if filter_metodo:
        historial = historial.filter(metodo_pago=filter_metodo)
    
    # Filtrar por fecha
    if filter_fecha:
        historial = historial.filter(fecha_venta__date=filter_fecha)
    
    # Calcular estadísticas
    stats = historial.aggregate(
        total_monto=Sum('Monto'),
        total_ventas=Count('id_registro')
    )
    
    # Paginación
    paginator = Paginator(historial, items_per_page)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'AllHV': page_obj,
        'total_items': paginator.count,
        'search_query': search_query,
        'filter_metodo': filter_metodo,
        'filter_fecha': filter_fecha,
        'items_per_page': items_per_page,
        'total_monto': stats['total_monto'] or 0,
        'total_ventas': stats['total_ventas'] or 0,
    }
    
    return render(request, 'templates_ventas/historial_ventas.html', context)