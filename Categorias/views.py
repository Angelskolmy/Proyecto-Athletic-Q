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
        return redirect('Perfil')
    
    # Obtener parámetro de búsqueda
    search_query = request.GET.get('search', '').strip()
    page_number = request.GET.get('page', 1)

    # Filtrar categorías
    categorias = categoria.objects.all().order_by('Id_categoria')
    
    if search_query:
        categorias = categorias.filter(
            Q(Nombre__icontains=search_query) |
            Q(Estado__icontains=search_query)
        )

    # Crear paginador - 15 registros por página
    paginator = Paginator(categorias, 15)
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
    }

    return render(request, "templates_categoria/categorias.html", context)


@transaction.atomic
def CrearCategoria(request):
    if request.method == 'POST':
        form = CrearCategoriaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Categoría creada exitosamente.')
                return redirect('Categorias')
            except Exception as e:
                messages.error(request, f'Error al crear la categoría: {str(e)}')
    else:
        form = CrearCategoriaForm()

    return render(request, 'templates_categoria/crear_categorias.html', {'form': form})


@transaction.atomic
def EditarCategoria(request, Id_categoria):
    categoria_obj = get_object_or_404(categoria, Id_categoria=Id_categoria)
    
    # Contar productos asociados
    from Productos.models import producto
    productos_count = producto.objects.filter(Catego_Id=categoria_obj).count()
    
    if request.method == 'POST':
        form = EditarCategoriaForm(request.POST, instance=categoria_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('Categorias')
    else:
        form = EditarCategoriaForm(instance=categoria_obj)
    
    context = {
        'form': form,
        'categoria': categoria_obj,
        'productos_count': productos_count,
    }
    
    return render(request, 'templates_categoria/editar_categorias.html', context)