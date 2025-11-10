from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
from .models import categoria
from .forms import CrearCategoriaForm, EditarCategoriaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')

@transaction.atomic
def ListarCategorias(request):
    if not request.user.has_perm('Categorias.view_categoria'):
        messages.warning(request, "No tienes permiso para acceder a esta sección.")
        return redirect('Perfil')  # URL de perfil
    
    # Obtener parámetros de búsqueda y paginación
    search_query = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)
    items_per_page = request.GET.get('items_per_page', 10)

    # Filtrar categorías
    categorias = categoria.objects.all().order_by('Id_categoria')
    
    if search_query:
        categorias = categorias.filter(
            Q(Nombre__icontains=search_query) |
            Q(Estado__icontains=search_query)
        )

    # Crear paginador
    paginator = Paginator(categorias, items_per_page)
    page_obj = paginator.get_page(page_number)

    # Calcular rango de resultados mostrados
    start_index = (page_obj.number - 1) * paginator.per_page + 1
    end_index = min(start_index + paginator.per_page - 1, paginator.count)

    context = {
        'Categorias': page_obj,
        'total_items': paginator.count,
        'start_index': start_index,
        'end_index': end_index,
        'search_query': search_query,
        'items_per_page': items_per_page
    }

    return render(request, "templates_categoria/categorias.html", context)

@transaction.atomic
def CrearCategoria(request):
    if request.method == 'POST':
        form = CrearCategoriaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Categoría creada exitosamente',
                    'redirect': '/Categorias/'
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Error al crear la categoría: {str(e)}'
                }, status=400)
    else:
        form = CrearCategoriaForm()

    return render(request, 'templates_categoria/crear_categoria.html', {'form': form})

@transaction.atomic
def EditarCategoria(request, id):
    categoria_obj = get_object_or_404(categoria, Id_categoria=id)
    
    if request.method == 'POST':
        form = EditarCategoriaForm(request.POST, instance=categoria_obj)
        if form.is_valid():
            try:
                form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Categoría actualizada exitosamente',
                    'redirect': '/Categorias/'
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Error al actualizar la categoría: {str(e)}'
                }, status=400)
    else:
        form = EditarCategoriaForm(instance=categoria_obj)

    return render(request, 'templates_categoria/editar_categoria.html', {
        'categoria': categoria_obj,
        'form': form
    })
