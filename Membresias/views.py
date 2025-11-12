from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta, date 
from .models import Membresia
from .forms import MembresiaForm
from Empleados.models import User_Empleados
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')

@transaction.atomic
def ListarMembresias(request):  
    # Obtener parámetros de búsqueda y filtro
    search_query = request.GET.get('search', '').strip()
    filter_type = request.GET.get('filter', '')
    page_number = request.GET.get('page', 1)
    items_per_page = int(request.GET.get('items_per_page', 10))

    # Obtener todas las membresías
    membresias = Membresia.objects.select_related('id_usuario').all().order_by('-Id_membresia')
    
    # Aplicar búsqueda por cliente
    if search_query:
        search_filters = Q(id_usuario__first_name__icontains=search_query) | \
                        Q(id_usuario__last_name__icontains=search_query) | \
                        Q(id_usuario__email__icontains=search_query)
        
        # Para cédula, verificar si es numérico
        if search_query.isdigit():
            search_filters |= Q(id_usuario__Cedula=int(search_query))
        
        # Para ID de membresía
        if search_query.isdigit():
            search_filters |= Q(Id_membresia=int(search_query))
            
        membresias = membresias.filter(search_filters)

    # Aplicar filtros
    if filter_type:
        today = timezone.now().date()
        if filter_type == 'activa':
            membresias = membresias.filter(Estado='Activo', Fecha_fin__gte=today)
        elif filter_type == 'vencida':
            membresias = membresias.filter(Fecha_fin__lt=today)
        elif filter_type == 'porvencer':
            next_week = today + timedelta(days=7)
            membresias = membresias.filter(Estado='Activo', Fecha_fin__lte=next_week, Fecha_fin__gte=today)

    # Crear paginador
    paginator = Paginator(membresias, items_per_page)
    page_obj = paginator.get_page(page_number)

    context = {
        'AllMebs': page_obj,
        'total_items': paginator.count,
        'search_query': search_query,
        'filter_type': filter_type,
        'items_per_page': items_per_page,
    }

    return render(request, "templates_membresias/membresias.html", context)

@transaction.atomic
def CrearMembresia(request):
    if request.method == 'POST':
        form = MembresiaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                membresia = form.save(commit=False)
                
                tipo_membresia = membresia.For_Id_tipo_membresia
                
                duracion_meses = tipo_membresia.Duracion_meses
                
                membresia.Fecha_inicio = timezone.now()
                
                fecha_inicio_date = timezone.now().date()
                membresia.Fecha_fin = fecha_inicio_date + timedelta(days=30 * duracion_meses)

                membresia.save()
                
                messages.success(request, 'Membresía creada exitosamente')
                return redirect('Membresias')
                
            except Exception as e:
                messages.error(request, f'Error al crear la membresía: {str(e)}')
                print(f"Error detallado: {e}")
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = MembresiaForm()

    return render(request, 'templates_membresias/crear_membresias.html', {'form': form})

@transaction.atomic
@permission_required('Membresias.change_membresia', login_url='Membresias')
def EditarMembresia(request, id):
    membresia = get_object_or_404(Membresia, Id_membresia=id)
    
    if request.method == 'POST':
        form = MembresiaForm(request.POST, instance=membresia)
        if form.is_valid():
            try:
                membresia = form.save(commit=False)
                
                # Recalcular fecha fin si cambió la duración
                if membresia.Duracion_meses:
                    fecha_inicio = membresia.Fecha_inicio.date() if hasattr(membresia.Fecha_inicio, 'date') else membresia.Fecha_inicio
                    membresia.Fecha_fin = fecha_inicio + timedelta(days=30 * membresia.Duracion_meses)
                
                membresia.save()
                
                messages.success(request, 'Membresía actualizada exitosamente')
                return redirect('Membresias')
                
            except Exception as e:
                messages.error(request, f'Error al actualizar la membresía: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = MembresiaForm(instance=membresia)

    context = {
        'form': form,
        'membresia': membresia,
    }
    
    return render(request, 'templates_membresias/editar_membresias.html', context)

@transaction.atomic
def DetalleMembresia(request, id):
    membresia = get_object_or_404(Membresia, Id_membresia=id)
    
    # Obtener la fecha actual
    today = timezone.now().date()
    
    # CORREGIR: Extraer fechas correctamente
    # Fecha_inicio es DateTimeField - extraer solo la fecha
    if hasattr(membresia.Fecha_inicio, 'date'):
        fecha_inicio = membresia.Fecha_inicio.date()
    else:
        fecha_inicio = membresia.Fecha_inicio
    
    # Fecha_fin es DateField - usar directamente
    fecha_fin = membresia.Fecha_fin
    
    # CALCULAR DÍAS TRANSCURRIDOS Y RESTANTES
    if fecha_inicio and isinstance(fecha_inicio, date):
        dias_transcurridos = (today - fecha_inicio).days
        dias_transcurridos = max(0, dias_transcurridos)  # No permitir negativos
    else:
        dias_transcurridos = 0
    
    if fecha_fin and isinstance(fecha_fin, date):
        dias_restantes = (fecha_fin - today).days
        dias_restantes = max(0, dias_restantes)  # No permitir negativos
    else:
        dias_restantes = 0
    
    # CALCULAR PROGRESO DE LA MEMBRESÍA
    duracion_total_dias = membresia.Duracion_meses * 30  # Aproximado
    
    if duracion_total_dias > 0 and dias_transcurridos >= 0:
        progreso_porcentaje = (dias_transcurridos / duracion_total_dias) * 100
        progreso_porcentaje = min(100, max(0, progreso_porcentaje))  # Entre 0 y 100
    else:
        progreso_porcentaje = 0
    
    # Redondear progreso
    progreso_porcentaje = round(progreso_porcentaje, 1)
    
    # DETERMINAR ESTADO VISUAL
    if membresia.Estado == 'Activo' and fecha_fin >= today:
        estado_visual = 'Activa'
        estado_clase = 'success'
    elif fecha_fin < today:
        estado_visual = 'Vencida'
        estado_clase = 'danger'
    else:
        estado_visual = membresia.Estado
        estado_clase = 'secondary'
    
    # DEBUG: Para verificar valores
    print(f"\n=== DEBUG MEMBRESÍA {id} ===")
    print(f"Fecha inicio: {fecha_inicio} (tipo: {type(fecha_inicio)})")
    print(f"Fecha fin: {fecha_fin} (tipo: {type(fecha_fin)})")
    print(f"Fecha hoy: {today}")
    print(f"Duración meses: {membresia.Duracion_meses}")
    print(f"Duración total días: {duracion_total_dias}")
    print(f"Días transcurridos: {dias_transcurridos}")
    print(f"Días restantes: {dias_restantes}")
    print(f"Progreso: {progreso_porcentaje}%")
    print(f"Estado: {estado_visual}")
    print("========================\n")
    
    context = {
        'membresia': membresia,
        'dias_restantes': dias_restantes,
        'dias_transcurridos': dias_transcurridos,
        'estado_visual': estado_visual,
        'estado_clase': estado_clase,
        'progreso_porcentaje': progreso_porcentaje,
        'today': today
    }
    
    return render(request, 'templates_membresias/detalle_membresias.html', context)
