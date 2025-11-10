from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.models import Group
from .models import User_Empleados
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from .forms import EmpleadoForm

@login_required(login_url='login')
@permission_required('Empleados.view_user_empleados', login_url='home')

#@permission_required('Empleados.view_suariogym', login_url='home') este permiso puede hacer todo el view si ese usuario tiene ese permiso
@permission_required('Empleados.usariogym', login_url='login') # este permiso solo sirve para mirar el perfil 
def UsersGym(request): 
    return render(request,'templates_perfil/perfil.html')

@transaction.atomic
def ListarEmpleados(request):
    # Obtener parámetros de búsqueda, filtro y paginación
    search_query = request.GET.get('search', '').strip() 
    filter_type = request.GET.get('filter', '')
    page_number = request.GET.get('page', 1)
    items_per_page = int(request.GET.get('items_per_page', 10))

    # Obtener todos los empleados
    empleados = User_Empleados.objects.all().order_by('id')
    
    # Aplicar búsqueda por nombre, apellido o cédula
    if search_query:
        print(f"DEBUG - Búsqueda: '{search_query}'")  # Debug temporal
        
        # Crear filtros de búsqueda
        search_filters = Q(first_name__icontains=search_query) | \
                        Q(last_name__icontains=search_query) | \
                        Q(email__icontains=search_query) | \
                        Q(username__icontains=search_query)
        
        # Para búsqueda por cédula, verificar si es numérico
        if search_query.isdigit():
            search_filters |= Q(Cedula=int(search_query))
        
        empleados = empleados.filter(search_filters)

    # Aplicar filtros
    if filter_type:
        if filter_type == 'active':
            empleados = empleados.filter(is_active=True)
        elif filter_type == 'inactive':
            empleados = empleados.filter(is_active=False)
        elif filter_type == 'admin':
            empleados = empleados.filter(is_superuser=True)
        elif filter_type.startswith('group_'):
            # Filtrar por grupo específico
            group_id = filter_type.replace('group_', '')
            try:
                empleados = empleados.filter(groups__id=group_id).distinct()
            except ValueError:
                pass

    # Crear paginador
    paginator = Paginator(empleados, items_per_page)
    page_obj = paginator.get_page(page_number)

    # Obtener todos los grupos para el filtro
    grupos_disponibles = Group.objects.all().order_by('name')

    context = {
        'Empleados': page_obj,
        'total_items': paginator.count,
        'search_query': search_query,
        'filter_type': filter_type,
        'items_per_page': items_per_page,
        'grupos_disponibles': grupos_disponibles,
    }

    return render(request, "templates_usuarios/usuarios.html", context)

@transaction.atomic
def CrearEmpleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                empleado = form.save(commit=False)
                empleado.set_password(form.cleaned_data['password'])
                empleado.save()
                
                # Asignar grupo/rol
                if form.cleaned_data['groups']:
                    empleado.groups.add(form.cleaned_data['groups'])
                
                return JsonResponse({
                    'success': True,
                    'message': 'Usuario creado exitosamente',
                    'redirect': '/Empleados/',
                    'show_fingerprint_modal': True,  # Señal para mostrar modal de huella
                    'user_id': empleado.id
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Error al crear el usuario: {str(e)}'
                }, status=400)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Datos inválidos',
                'errors': form.errors
            }, status=400)
    else:
        form = EmpleadoForm()

    return render(request, 'templates_usuarios/crear_usuarios.html', {'form': form})

@transaction.atomic
def EditarEmpleado(request, id):
    empleado = get_object_or_404(User_Empleados, id=id)
    
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            try:
                empleado = form.save(commit=False)
                
                # Solo actualizar contraseña si se proporcionó
                if form.cleaned_data['password']:
                    empleado.set_password(form.cleaned_data['password'])
                
                empleado.save()
                
                # Actualizar grupos (limpiar y agregar el seleccionado)
                empleado.groups.clear()
                if form.cleaned_data['groups']:
                    empleado.groups.add(form.cleaned_data['groups'])
                
                return JsonResponse({
                    'success': True,
                    'message': 'Usuario actualizado exitosamente',
                    'redirect': '/Empleados/'
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Error al actualizar el usuario: {str(e)}'
                }, status=400)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Datos inválidos',
                'errors': form.errors
            }, status=400)
    else:
        form = EmpleadoForm(instance=empleado)

    return render(request, 'templates_usuarios/editar_usuarios.html', {
        'empleado': empleado,
        'form': form
    })

# Nueva vista para registro de huella
@transaction.atomic
def RegistrarHuella(request, user_id):
    if request.method == 'POST':
        try:
            empleado = get_object_or_404(User_Empleados, id=user_id)
            huella_data = request.POST.get('huella_data')
            attempt_number = int(request.POST.get('attempt_number', 1))
            
            if huella_data:  # Si se leyó correctamente la huella
                if attempt_number >= 3:
                    # Después de 3 intentos exitosos, guardar la huella
                    empleado.Huella_id = hash(huella_data) % 1000000  # Generar ID único
                    empleado.save()
                    
                    return JsonResponse({
                        'success': True,
                        'message': '¡Huella registrada exitosamente!',
                        'attempts': 3,
                        'completed': True
                    })
                else:
                    return JsonResponse({
                        'success': True,
                        'message': f'Intento {attempt_number}/3 registrado correctamente',
                        'attempts': attempt_number,
                        'completed': False
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'No se pudo leer la huella. Intente nuevamente.'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al registrar huella: {str(e)}'
            }, status=400)
    
    return JsonResponse({'message': 'Método no permitido'}, status=405)