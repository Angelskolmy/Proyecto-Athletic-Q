from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from .models import Membresia
from .forms import MembresiaForm
from Empleados.models import User_Empleados
from Tipo_membresia.models import TipoMembresia
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
@permission_required('Membresias.view_membresia', login_url='login')
@transaction.atomic
def ListarMembresias(request):  
    search_query = request.GET.get('search', '').strip()
    filter_type = request.GET.get('filter', '')
    page_number = request.GET.get('page', 1)
    items_per_page = int(request.GET.get('items_per_page', 10))

    #  USAR select_related PARA OPTIMIZAR
    membresias = Membresia.objects.select_related(
        'id_usuario', 
        'For_Id_tipo_membresia'
    ).all().order_by('-Id_membresia')
    
    if search_query:
        search_filters = Q(id_usuario__first_name__icontains=search_query) | \
                        Q(id_usuario__last_name__icontains=search_query) | \
                        Q(id_usuario__email__icontains=search_query)
        
        if search_query.isdigit():
            search_filters |= Q(id_usuario__Cedula=int(search_query))
            search_filters |= Q(Id_membresia=int(search_query))
            
        membresias = membresias.filter(search_filters)

    if filter_type:
        today = timezone.now().date()
        if filter_type == 'activa':
            membresias = membresias.filter(Estado='Activo', Fecha_fin__gte=today)
        elif filter_type == 'vencida':
            membresias = membresias.filter(Fecha_fin__lt=today)
        elif filter_type == 'porvencer':
            next_week = today + timedelta(days=7)
            membresias = membresias.filter(Estado='Activo', Fecha_fin__lte=next_week, Fecha_fin__gte=today)

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


@login_required(login_url='login')
@permission_required('Membresias.add_membresia', login_url='Membresias')
@transaction.atomic
def CrearMembresia(request):
    if request.method == 'POST':
        form = MembresiaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                membresia = form.save(commit=False)
                
                #  OBTENER TIPO DE MEMBRESÍA
                tipo_membresia = membresia.For_Id_tipo_membresia
                
                #  LEER DURACIÓN DEL TIPO (NO de membresia)
                duracion_meses = tipo_membresia.Duracion_meses
                
                #  ESTABLECER FECHA DE INICIO
                membresia.Fecha_inicio = timezone.now()
                
                #  CALCULAR FECHA DE FIN usando relativedelta
                fecha_inicio_date = timezone.now().date()
                membresia.Fecha_fin = fecha_inicio_date + relativedelta(months=duracion_meses)

                membresia.save()
                
                messages.success(
                    request, 
                    f'Membresía creada: {tipo_membresia.Nombre} - Vence el {membresia.Fecha_fin.strftime("%d/%m/%Y")}'
                )
                return redirect('Membresias')
                
            except Exception as e:
                messages.error(request, f'Error al crear la membresía: {str(e)}')
                print(f"Error detallado: {e}")
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = MembresiaForm()

    return render(request, 'templates_membresias/crear_membresias.html', {'form': form})

@login_required(login_url='login')
@permission_required('Membresias.change_membresia', login_url='Membresias')
@transaction.atomic
def EditarMembresia(request, id):
    membresia = get_object_or_404(Membresia, Id_membresia=id)
    
    if request.method == 'POST':
        form = MembresiaForm(request.POST, request.FILES, instance=membresia)
        if form.is_valid():
            try:
                membresia_actualizada = form.save(commit=False)
                
                # Asegurar que no se cambien estos campos
                membresia_actualizada.id_usuario = membresia.id_usuario
                membresia_actualizada.For_Id_tipo_membresia = membresia.For_Id_tipo_membresia
                membresia_actualizada.Fecha_inicio = membresia.Fecha_inicio
                membresia_actualizada.Fecha_fin = membresia.Fecha_fin
                
                membresia_actualizada.save()
                
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


@login_required(login_url='login')
@permission_required('Membresias.view_membresia', login_url='Membresias')
@transaction.atomic
def DetalleMembresia(request, id):
    #  OBTENER MEMBRESÍA CON RELACIONES
    membresia = get_object_or_404(
        Membresia.objects.select_related('id_usuario', 'For_Id_tipo_membresia'),
        Id_membresia=id
    )
    
    today = timezone.now().date()
    
    #  EXTRAER FECHAS
    if hasattr(membresia.Fecha_inicio, 'date'):
        fecha_inicio = membresia.Fecha_inicio.date()
    else:
        fecha_inicio = membresia.Fecha_inicio
    
    fecha_fin = membresia.Fecha_fin
    
    #  CALCULAR DÍAS
    if fecha_inicio and isinstance(fecha_inicio, date):
        dias_transcurridos = (today - fecha_inicio).days
        dias_transcurridos = max(0, dias_transcurridos)
    else:
        dias_transcurridos = 0
    
    if fecha_fin and isinstance(fecha_fin, date):
        dias_restantes = (fecha_fin - today).days
        dias_restantes = max(0, dias_restantes)
    else:
        dias_restantes = 0
    
    #  OBTENER DURACIÓN DEL TIPO DE MEMBRESÍA
    duracion_meses = membresia.For_Id_tipo_membresia.Duracion_meses
    duracion_total_dias = duracion_meses * 30
    
    #  CALCULAR PROGRESO
    if duracion_total_dias > 0 and dias_transcurridos >= 0:
        progreso_porcentaje = (dias_transcurridos / duracion_total_dias) * 100
        progreso_porcentaje = min(100, max(0, progreso_porcentaje))
    else:
        progreso_porcentaje = 0
    
    progreso_porcentaje = round(progreso_porcentaje, 1)
    
    #  DETERMINAR ESTADO VISUAL
    if membresia.Estado == 'Activo' and fecha_fin >= today:
        estado_visual = 'Activa'
        estado_clase = 'success'
    elif fecha_fin < today:
        estado_visual = 'Vencida'
        estado_clase = 'danger'
    else:
        estado_visual = membresia.Estado
        estado_clase = 'secondary'
    
    #  CALCULAR PRECIO MENSUAL
    precio_mensual = membresia.For_Id_tipo_membresia.Precio / duracion_meses if duracion_meses > 0 else 0
    
    context = {
        'membresia': membresia,
        'dias_restantes': dias_restantes,
        'dias_transcurridos': dias_transcurridos,
        'estado_visual': estado_visual,
        'estado_clase': estado_clase,
        'progreso_porcentaje': progreso_porcentaje,
        'precio_mensual': precio_mensual,
        'today': today
    }
    
    return render(request, 'templates_membresias/detalle_membresias.html', context)