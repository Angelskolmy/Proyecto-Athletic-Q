from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
from .models import categoria

@transaction.atomic
def ListarCategorias(request):
    # Obtener parámetros de búsqueda y paginación
    search_query = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)
    items_per_page = request.GET.get('items_per_page', 10)  # Por defecto 10 items por página

    # Filtrar categorías
    categorias = categoria.objects.all().order_by('Nombre')
    
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
        try:
            nueva_categoria = categoria.objects.create(
                Nombre=request.POST.get('nombre'),
                Estado='Activo'  # Estado por defecto al crear
            )
            return JsonResponse({
                'status': 'success',
                'message': 'Categoría creada correctamente',
                'redirect': '/Categorias/'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error al crear la categoría: {str(e)}'
            }, status=400)

    return render(request, 'templates_categoria/crear_categoria.html')

@transaction.atomic
def EditarCategoria(request, id):
    categoria_obj = get_object_or_404(categoria, Id_categoria=id)
    
    if request.method == 'POST':
        try:
            categoria_obj.Nombre = request.POST.get('nombre')
            categoria_obj.Estado = request.POST.get('estado').capitalize()
            categoria_obj.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Categoría actualizada correctamente',
                'redirect': '/Categorias/'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error al actualizar la categoría: {str(e)}'
            }, status=400)

    return render(request, 'templates_categoria/editar_categoria.html', {
        'categoria': categoria_obj
    })