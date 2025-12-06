from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone

from .models import TipoMembresia
from .forms import TipoMembresiaForm
from Historial.models import Historial_usuario
from Membresias.models import Membresia


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
            Roling3 = form.save()

            # HISTORIAL (tomado del view 2)
            histuser4 = request.user
            histMod4 = 'Tipo_Membresias'
            histMovs4 = 'ingresar'
            histFech4 = timezone.now().date()
            histNomb4 = Roling3.Nombre
            histId4 = Roling3.Id_tipo_membresia

            Historial_usuario.objects.create(
                id_usuario=histuser4,
                TIpo_Movimiento=histMovs4,
                Modulo=histMod4,
                Nombre_Objeto=histNomb4,
                Id_Objeto=histId4,
                Fecha_y_hora=histFech4,
            )

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

    # Estaba en el view 1, lo dejamos igual
    membresias_count = Membresia.objects.filter(For_Id_tipo_membresia=tipo).count()
    
    if request.method == 'POST':
        form = TipoMembresiaForm(request.POST, request.FILES, instance=tipo)
        if form.is_valid():
            Roling4 = form.save()

            # HISTORIAL (tomado del view 2)
            histuser5 = request.user
            histMod5 = 'Tipo_Membresias'
            histMovs5 = 'editar'
            histFech5 = timezone.now().date()
            histNomb5 = Roling4.Nombre
            histId5 = Roling4.Id_tipo_membresia

            Historial_usuario.objects.create(
                id_usuario=histuser5,
                TIpo_Movimiento=histMovs5,
                Modulo=histMod5,
                Nombre_Objeto=histNomb5,
                Id_Objeto=histId5,
                Fecha_y_hora=histFech5,
            )

            messages.success(request, 'Tipo de membresía actualizado exitosamente.')
            return redirect('TiposMembresia')
    else:
        form = TipoMembresiaForm(instance=tipo)
    
    return render(request, 'templates_tipo_membresia/editar_tipo_membresia.html', {
        'form': form,
        'tipo': tipo,
        'membresias_count': membresias_count,
    })
