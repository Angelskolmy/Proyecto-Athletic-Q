from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import TipoMembresia
from .forms import TipoMembresiaForm


@login_required(login_url='login')
@permission_required('Tipo_membresia.view_tipomembresia', login_url='login')
def listarTiposMembresia(request):
    search_query = request.GET.get('search', '').strip()
    filter_duracion = request.GET.get('duracion', '')
    page_number = request.GET.get('page', 1)

    tipos = TipoMembresia.objects.all().order_by('Duracion_meses', 'Precio')
    
    # Búsqueda
    if search_query:
        tipos = tipos.filter(
            Q(Nombre__icontains=search_query) |
            Q(Estado__icontains=search_query)
        )
    
    # Filtro por duración
    if filter_duracion:
        tipos = tipos.filter(Duracion_meses=filter_duracion)

    # Paginación - 15 registros
    paginator = Paginator(tipos, 15)
    page_obj = paginator.get_page(page_number)

    # Calcular rango
    start_index = (page_obj.number - 1) * paginator.per_page + 1
    end_index = min(start_index + paginator.per_page - 1, paginator.count)

    # Verificar si hay filtros
    hay_filtros = any([search_query, filter_duracion])

    context = {
        'TiposMembresia': page_obj,
        'total_items': paginator.count,
        'start_index': start_index,
        'end_index': end_index,
        'search_query': search_query,
        'filter_duracion': filter_duracion,
        'hay_filtros': hay_filtros,
    }
    
    return render(request, 'templates_tipo_membresia/tipo_membresia.html', context)


@login_required(login_url='login')
@permission_required('Tipo_membresia.add_tipomembresia', login_url='TiposMembresia')
@transaction.atomic
def crearTipoMembresia(request):
    if request.method == 'POST':
        form = TipoMembresiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de membresía creado exitosamente.')
            return redirect('TiposMembresia')
    else:  
        form = TipoMembresiaForm()
    
    return render(request, 'templates_tipo_membresia/crear_tipo_membresia.html', {'form': form})


@login_required(login_url='login')
@permission_required('Tipo_membresia.change_tipomembresia', login_url='TiposMembresia')
@transaction.atomic
def editarTipoMembresia(request, Id_tipo_membresia):
    tipo = get_object_or_404(TipoMembresia, Id_tipo_membresia=Id_tipo_membresia)
    
    # Contar membresías asociadas
    from Membresias.models import Membresia
    membresias_count = Membresia.objects.filter(For_Id_tipo_membresia=tipo).count()
    
    if request.method == 'POST':
        form = TipoMembresiaForm(request.POST, request.FILES, instance=tipo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de membresía actualizado exitosamente.')
            return redirect('TiposMembresia')
    else:
        form = TipoMembresiaForm(instance=tipo)
    
    return render(request, 'templates_tipo_membresia/editar_tipo_membresia.html', {
        'form': form,
        'tipo': tipo,
        'membresias_count': membresias_count,
    })