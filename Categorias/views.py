from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import categoria
from .forms import CrearCategoriaForm, EditarCategoriaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from Historial.models import Historial_usuario


@login_required(login_url='login')
@permission_required('Categorias.view_categoria', login_url='Perfil')
@transaction.atomic
def ListarCategorias(request):
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


@login_required(login_url='login')
@permission_required('Categorias.add_categoria', login_url='Categorias')
@transaction.atomic
def CrearCategoria(request):
    if request.method == 'POST':
        form = CrearCategoriaForm(request.POST)
        if form.is_valid():
            try:
                nueva_categoria = form.save()
                
                # ================================
                # HISTORIAL DE MOVIMIENTOS - CREAR
                # ================================
                histVend = request.user
                histMod = 'categorías'
                histMovs = 'ingresar'
                histFech = timezone.now().date()
                histNomb = nueva_categoria.Nombre[:50]
                histId = nueva_categoria.Id_categoria

                try:
                    hu = Historial_usuario.objects.create(
                        id_usuario=histVend,
                        TIpo_Movimiento=histMovs,
                        Modulo=histMod,
                        Nombre_Objeto=histNomb,
                        Id_Objeto=histId,
                        Fecha_y_hora=histFech,
                    )
                    print("DEBUG: Historial_usuario created Id_historial =", getattr(hu, 'Id_historial', None))
                except Exception as exc:
                    import traceback
                    traceback.print_exc()
                    messages.warning(request, f'No se pudo registrar en historial de movimientos: {exc}')

                messages.success(request, 'Categoría creada exitosamente.')
                return redirect('Categorias')
            except Exception as e:
                messages.error(request, f'Error al crear la categoría: {str(e)}')
    else:
        form = CrearCategoriaForm()

    return render(request, 'templates_categoria/crear_categorias.html', {'form': form})


@login_required(login_url='login')
@permission_required('Categorias.change_categoria', login_url='Categorias')
@transaction.atomic
def EditarCategoria(request, Id_categoria):
    categoria_obj = get_object_or_404(categoria, Id_categoria=Id_categoria)
    
    # Contar productos asociados
    from Productos.models import producto
    productos_count = producto.objects.filter(Catego_Id=categoria_obj).count()
    
    if request.method == 'POST':
        form = EditarCategoriaForm(request.POST, instance=categoria_obj)
        if form.is_valid():
            categoria_editada = form.save()
            
            # ================================
            # HISTORIAL DE MOVIMIENTOS - EDITAR
            # ================================
            histVend = request.user
            histMod = 'categorías'
            histMovs = 'editar'
            histFech = timezone.now().date()
            histNomb = categoria_editada.Nombre[:50]
            histId = categoria_editada.Id_categoria

            try:
                hu = Historial_usuario.objects.create(
                    id_usuario=histVend,
                    TIpo_Movimiento=histMovs,
                    Modulo=histMod,
                    Nombre_Objeto=histNomb,
                    Id_Objeto=histId,
                    Fecha_y_hora=histFech,
                )
                print("DEBUG: Historial_usuario created Id_historial =", getattr(hu, 'Id_historial', None))
            except Exception as exc:
                import traceback
                traceback.print_exc()
                messages.warning(request, f'No se pudo registrar en historial de movimientos: {exc}')

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