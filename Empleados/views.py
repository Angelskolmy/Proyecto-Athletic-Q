import json
import requests
import qrcode
import base64

from io import BytesIO
from base64 import b64encode
from datetime import date, time, timedelta, datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.db.models import Q
from django.db.models import Exists, OuterRef
from django.contrib.auth.models import Group

from .forms import EmpleadoForm
from .models import User_Empleados
from Core_session.models import HuellaCaptura
from Asistencia.models import Asistencia
from Membresias.models import Membresia
from Rutinas.models import Rutina


@permission_required("Empleados.view_user_empleados", raise_exception=True)
@transaction.atomic
def ListarEmpleados(request):
    
    # Verificar si hay mensaje pendiente de la creación
    mensaje_exito = request.session.pop('mensaje_exito', None)
    if mensaje_exito:
        messages.success(request, mensaje_exito)
        
    # Obtener parámetros de búsqueda, filtro y paginación
    search_query = request.GET.get("search", "").strip()
    filter_type = request.GET.get("filter", "")
    page_number = request.GET.get("page", 1)
    items_per_page = int(request.GET.get("items_per_page", 10))

    empleados = (
        User_Empleados.objects
        .annotate(tiene_huella=Exists(
            HuellaCaptura.objects.filter(id_usuario=OuterRef('pk'))
        ))
        .order_by('id')
    )

    if request.user.groups.filter(name="Empleados").exists():
        empleados = empleados.filter(groups__name="Usuarios")

    # Búsqueda por nombre, apellido, correo o cédula
    if search_query:
        search_filters = (
            Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(email__icontains=search_query)
        )
        if search_query.isdigit():
            search_filters |= Q(Cedula=int(search_query))
        empleados = empleados.filter(search_filters)

    # Filtros adicionales
    if filter_type:
        if filter_type == "active":
            empleados = empleados.filter(is_active=True)
        elif filter_type == "inactive":
            empleados = empleados.filter(is_active=False)
        elif filter_type.startswith("group_"):
            group_id = filter_type.replace("group_", "")
            try:
                empleados = empleados.filter(groups__id=group_id).distinct()
            except ValueError:
                pass

    paginator = Paginator(empleados, items_per_page)
    page_obj = paginator.get_page(page_number)

    context = {
        "Empleados": page_obj,
        "total_items": paginator.count,
        "search_query": search_query,
        "filter_type": filter_type,
        "items_per_page": items_per_page,
        "grupos_disponibles": Group.objects.all().order_by("name"),
    }
    return render(request, "templates_usuarios/usuarios.html", context)


@transaction.atomic
def CrearEmpleado(request):
    if request.method == "POST":
        form = EmpleadoForm(request.POST, request.FILES, usuario_actual=request.user)

        if form.is_valid():
            try:
                empleado = form.save(commit=False)

                # Flags requeridos por el modelo/auth
                empleado.is_superuser = False
                empleado.is_staff = True
                is_active_raw = form.cleaned_data.get("is_active")
                empleado.is_active = str(is_active_raw).lower() in ("true", "1", "yes", "on", "activo")

                # Asegurar fecha de creación para no enviar NULL
                if not empleado.date_joined:
                    empleado.date_joined = timezone.now()

                # Guardar contraseña correctamente
                empleado.set_password(form.cleaned_data["password"])
                empleado.save()

                # Guardar grupo/rol
                if form.cleaned_data.get("groups"):
                    empleado.groups.add(form.cleaned_data["groups"])

                # Guardar mensaje en sesión para mostrar DESPUÉS del modal
                request.session['mensaje_exito'] = f'Usuario "{empleado.first_name} {empleado.last_name}" creado exitosamente.'

                url = f"{reverse('empleados_create')}?show_modal=1&emp_id={empleado.id}"
                return redirect(url)

            except Exception as e:
                transaction.set_rollback(True)
                messages.error(request, f"Error al crear empleado: {e}")
                return render(request, "templates_usuarios/crear_usuarios.html", {"form": form})

        messages.error(request, 'Error en el formulario. Revisa los campos marcados.')
        return render(request, "templates_usuarios/crear_usuarios.html", {"form": form})

    # GET: mostrar el formulario
    form = EmpleadoForm(usuario_actual=request.user)
    return render(request, "templates_usuarios/crear_usuarios.html", {"form": form})

@transaction.atomic
def EditarEmpleado(request, id):
    empleado = get_object_or_404(User_Empleados, id=id)
    
    if request.method == "POST":
        form = EmpleadoForm(request.POST, request.FILES, instance=empleado, usuario_actual=request.user)
        
        if form.is_valid():
            try:
                empleado_actualizado = form.save(commit=False)
                
                # Actualizar contraseña solo si se proporcionó una nueva
                password = form.cleaned_data.get('password')
                if password:
                    empleado_actualizado.set_password(password)
                
                # Manejar is_active
                is_active_raw = form.cleaned_data.get("is_active")
                if isinstance(is_active_raw, bool):
                    empleado_actualizado.is_active = is_active_raw
                else:
                    empleado_actualizado.is_active = str(is_active_raw).lower() in ("true", "1", "yes", "on", "activo")
                
                empleado_actualizado.save()
                
                # Actualizar grupo/rol
                grupo = form.cleaned_data.get('groups')
                if grupo:
                    empleado_actualizado.groups.clear()
                    empleado_actualizado.groups.add(grupo)
                
                # Mensaje de éxito
                messages.success(request, f'Usuario "{empleado_actualizado.first_name} {empleado_actualizado.last_name}" actualizado correctamente.')
                return redirect('Empleados')
                
            except Exception as e:
                transaction.set_rollback(True)
                messages.error(request, f'Error al actualizar el usuario: {str(e)}')
                return redirect('empleados_edit', id=id)
        else:
            # Si el formulario no es válido
            messages.error(request, 'Error en el formulario. Revisa los campos marcados.')
    else:
        form = EmpleadoForm(instance=empleado, usuario_actual=request.user)
    
    context = {
        'form': form,
        'empleado': empleado
    }
    
    return render(request, "templates_usuarios/editar_usuarios.html", context)

@login_required(login_url='login')
@permission_required("Empleados.view_user_empleados", raise_exception=True)
def DetalleEmpleado(request, id):
    """Vista para ver el detalle completo de un usuario"""
    empleado = get_object_or_404(
        User_Empleados.objects.prefetch_related('groups'),
        id=id
    )
    
    # Verificar si tiene huella registrada
    tiene_huella = HuellaCaptura.objects.filter(id_usuario=empleado).exists()
    
    # Obtener membresía activa (si existe)
    membresia_activa = Membresia.objects.filter(
        id_usuario=empleado,
        Estado='Activo'
    ).select_related('For_Id_tipo_membresia').first()
    
    # Contar asistencias del mes actual
    from datetime import date
    hoy = date.today()
    asistencias_mes = Asistencia.objects.filter(
        id_usuario=empleado,
        fecha_entrada__year=hoy.year,
        fecha_entrada__month=hoy.month
    ).count()
    
    context = {
        'empleado': empleado,
        'tiene_huella': tiene_huella,
        'membresia_activa': membresia_activa,
        'asistencias_mes': asistencias_mes,
    }
    
    return render(request, 'templates_usuarios/detalle_usuarios.html', context)

def capturar_huella(request, empleado_id):
    empleado = get_object_or_404(User_Empleados, id=empleado_id)
    return render(request, "templates_huella/huella.html", {"empleado": empleado})

@csrf_exempt
def guardar_huellas(request):
    """
    Guarda huellas enviadas como FMD en formato XML (string).
    Espera JSON: { "usuario_id": <int>, "templates": ["<fmd_xml>", ...] }
    """
    if request.method != "POST":
        return JsonResponse({"error": "Solo POST"}, status=405)

    try:
        data = json.loads(request.body)
        usuario_id = data["usuario_id"]
        templates = data["templates"]
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({"error": "JSON inválido o faltan campos"}, status=400)

    try:
        empleado = User_Empleados.objects.get(id=usuario_id)
    except User_Empleados.DoesNotExist:
        return JsonResponse({"error": "Usuario no existe"}, status=404)

    if not templates:
        return JsonResponse({"error": "No hay huellas para guardar"}, status=400)

    # Verificar si la huella ya pertenece a otro usuario usando el matcher
    existentes = list(HuellaCaptura.objects.select_related("id_usuario").all())
    if existentes:
        enrolled_templates = [h.template for h in existentes]
        for tpl in templates:
            try:
                r = requests.post(
                    "http://localhost:5000/match",
                    json={"Candidate": tpl, "Enrolled": enrolled_templates},
                    timeout=10,
                )
                r.raise_for_status()
                match_resp = r.json()
            except Exception as e:
                return JsonResponse(
                    {"error": f"No se pudo verificar duplicado de huella: {e}"},
                    status=500,
                )

            if match_resp.get("ok"):
                idx = match_resp.get("match")
                if idx is not None and idx < len(existentes):
                    coincidencia = existentes[idx]
                    # Si coincide con otro usuario distinto, bloquear
                    if coincidencia.id_usuario_id and coincidencia.id_usuario_id != empleado.id:
                        usuario_conflicto = coincidencia.id_usuario
                        nombre_conflicto = f"{usuario_conflicto.first_name} {usuario_conflicto.last_name}".strip()
                        if not nombre_conflicto:
                            nombre_conflicto = usuario_conflicto.username or f"ID {usuario_conflicto.id}"
                        return JsonResponse(
                            {
                                "error": (
                                    f"La huella ya esta registrada para otro usuario "
                                    f"({nombre_conflicto}). Captura otra huella."
                                )
                            },
                            status=409,
                        )

    # Reemplazar huellas anteriores del empleado por las nuevas capturas
    HuellaCaptura.objects.filter(id_usuario=empleado).delete()
    HuellaCaptura.objects.bulk_create(
        [HuellaCaptura(id_usuario=empleado, template=t) for t in templates]
    )

    return JsonResponse({"ok": True, "guardadas": len(templates)})

@csrf_exempt
def validar_huella(request):
    if request.method != "POST":
        return JsonResponse({"error": "Solo POST"}, status=405)

    try:
        data = json.loads(request.body)
        candidato = data["candidate"]
    except Exception:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    huellas_qs = list(HuellaCaptura.objects.all().values("template", "id_usuario"))
    if not huellas_qs:
        return JsonResponse({"error": "No hay huellas registradas"}, status=404)

    payload = {
        "Candidate": candidato,
        "Enrolled": [h["template"] for h in huellas_qs],
    }
    try:
        r = requests.post("http://localhost:5000/match", json=payload, timeout=10)
        r.raise_for_status()
        match_resp = r.json()
    except Exception as e:
        return JsonResponse({"error": f"No se pudo contactar matcher: {e}"}, status=500)

    if not match_resp.get("ok"):
        return JsonResponse({"ok": False, "mensaje": "Sin coincidencia"})

    enroll_index = match_resp.get("match")
    # score = match_resp.get("score")  # <-- define score
    if enroll_index is None or enroll_index >= len(huellas_qs):
        return JsonResponse({"ok": False, "mensaje": "Sin coincidencia"})

    usuario_id = huellas_qs[enroll_index]["id_usuario"]
    usuario = User_Empleados.objects.filter(id=usuario_id).first()
    if not usuario:
        return JsonResponse({"ok": False, "mensaje": "Usuario no encontrado"})

    nombre = f"{usuario.first_name} {usuario.last_name}"

    hoy = timezone.localdate()  # o date.today() si usas USE_TZ=False
    ahora = timezone.now()
    hora_local = timezone.localtime(ahora).time()

    # Ventana horaria permitida: 5:00 - 22:00 (10 p.m.)
    if not (time(5, 0) <= hora_local < time(22, 0)):
        return JsonResponse({"ok": False, "mensaje": "Registro fuera de horario (5:00 a 22:00)."})

    # último registro abierto del usuario
    reg = Asistencia.objects.filter(
        id_usuario=usuario,
        fecha_salida__isnull=True
    ).order_by('-fecha_entrada').first()

    # Si tiene un registro sin salida de días anteriores, marcarlo pendiente y cerrarlo
    if reg and reg.fecha_entrada.date() < hoy:
        cierre_prev = datetime.combine(reg.fecha_entrada.date(), time(22, 0))
        if timezone.is_naive(cierre_prev):
            cierre_prev = timezone.make_aware(cierre_prev, timezone.get_current_timezone())
        reg.fecha_salida = cierre_prev
        reg.estado = "Pendiente"
        reg.save(update_fields=["fecha_salida", "estado"])
        reg = None  # permite crear nuevo registro hoy

    # evita duplicar si acaba de marcar hace pocos segundos
    if reg and (ahora - reg.fecha_entrada) < timedelta(seconds=30):
        # opcional: simplemente retornar sin crear nada
        mensaje_asistencia = "Marca ya registrada hace segundos"
    else:
        if reg and reg.fecha_entrada.date() == hoy:
            # cerrar salida
            reg.fecha_salida = ahora
            reg.estado = "Salida"
            reg.save(update_fields=["fecha_salida", "estado"])
            mensaje_asistencia = "Salida registrada"
        else:
            # crear nueva entrada
            reg = Asistencia.objects.create(
                id_usuario=usuario,
                rol=(usuario.groups.first().name if usuario.groups.exists() else ""),
                fecha_entrada=ahora,
                fecha_salida=None,
                estado="Entrada"
            )
            mensaje_asistencia = "Entrada registrada"

    return JsonResponse({
        "ok": True,
        "usuario": nombre,
        "asistencia": mensaje_asistencia,
        "entrada": reg.fecha_entrada,
        "salida": reg.fecha_salida,
    })

@login_required(login_url="login")
def MiPerfil(request):
    """Vista de perfil para administradores y empleados"""
    usuario = request.user

    qr_image = generar_qr_asistencia(
        request,
        usuario_id=usuario.id,
        usuario_nombre=usuario.first_name or usuario.username
    )

    membresias = Membresia.objects.filter(id_usuario=usuario).order_by("-Fecha_inicio")
    grupos = usuario.groups.all()
    tiene_huella = HuellaCaptura.objects.filter(id_usuario=usuario).exists()

    context = {
        "usuario": usuario,
        "membresias": membresias,
        'qr_image': qr_image,
        "grupos": grupos,
        "tiene_huella": tiene_huella,
    }
    return render(request, "templates_perfil/mi_perfil.html",context)

# @permission_required('Empleados.view_suariogym', login_url='home') este permiso puede hacer todo el view si ese usuario tiene ese permiso
@permission_required('Empleados.usariogym', raise_exception=True)
def UsersGym(request): 
    """Vista principal del cliente/usuario del gimnasio"""
    usuario = request.user

    # --------- LÓGICA DE QR (versión 1) ----------
    user = usuario
    membresia = Membresia.objects.filter(id_usuario=user).first()

    qr_image = generar_qr_asistencia(
        request,
        usuario_id=user.id,
        usuario_nombre=user.first_name or user.username
    )
    # --------------------------------------------

    # Obtener membresía activa del usuario (versión 2)
    membresia_activa = Membresia.objects.filter(
        id_usuario=usuario,
        Estado='Activo'
    ).select_related('For_Id_tipo_membresia').first()
    
    # Calcular días restantes si hay membresía
    dias_restantes = 0
    progreso = 0
    if membresia_activa:
        from datetime import date
        hoy = date.today()
        if membresia_activa.Fecha_fin >= hoy:
            dias_restantes = (membresia_activa.Fecha_fin - hoy).days
            # Calcular progreso
            fecha_inicio = membresia_activa.Fecha_inicio.date() if hasattr(membresia_activa.Fecha_inicio, 'date') else membresia_activa.Fecha_inicio
            total_dias = (membresia_activa.Fecha_fin - fecha_inicio).days
            dias_transcurridos = (hoy - fecha_inicio).days
            progreso = min(100, max(0, (dias_transcurridos / total_dias) * 100)) if total_dias > 0 else 0
    
    # Obtener rutinas activas
    rutinas = Rutina.objects.filter(Estado='Activo').order_by('Categoria', 'Nivel')
    
    # Agrupar rutinas por categoría
    rutinas_por_categoria = {}
    for rutina in rutinas:
        if rutina.Categoria not in rutinas_por_categoria:
            rutinas_por_categoria[rutina.Categoria] = []
        rutinas_por_categoria[rutina.Categoria].append(rutina)
    
    context = {
        'usuario': usuario,
        'membresia': membresia_activa,          # membresía activa (versión 2)
        'dias_restantes': dias_restantes,
        'progreso': round(progreso, 1),
        'rutinas': rutinas,
        'rutinas_por_categoria': rutinas_por_categoria,

        # claves de la versión 1 para no romper nada:
        'membresias': membresia,                # la primera que encontraba, sin filtrar por Estado
        'qr_image': qr_image,
    }
    
    return render(request, 'templates_perfil/datos.html', context)

def generar_qr_asistencia(request, usuario_id, usuario_nombre):
    # URL ABSOLUTA 
    url_qr = request.build_absolute_uri(
        reverse('validar_qr', args=[usuario_id])  # sin namespace si no lo usas
    )

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url_qr)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    qr_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return qr_image_base64

def validar_qr(request, usuario_id):
    usuario = get_object_or_404(User_Empleados, id=usuario_id)

    return render(
        request,
        "templates_perfil/validar_qr.html",
        {"usuario":usuario}
    )

@csrf_exempt
def registrar_asistencia_ajax(request):
    if request.method != "POST":
        return JsonResponse({"mensaje": "Solo POST"}, status=405)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"mensaje": "JSON inválido"}, status=400)

    raw = data.get("dato_qr")
    if not raw:
        return JsonResponse({"mensaje": "ID no recibido"}, status=400)

    # Si viene una URL, tomar el último segmento
    if isinstance(raw, str) and "/" in raw:
        raw = raw.strip("/").split("/")[-1]

    try:
        usuario_id = int(raw)
    except (TypeError, ValueError):
        return JsonResponse({"mensaje": "ID inválido"}, status=400)

    usuario = get_object_or_404(User_Empleados, id=usuario_id)
    hoy = timezone.localdate()
    ahora = timezone.now()
    hora_local = timezone.localtime(ahora).time()

    # Ventana horaria permitida: 5:00 - 22:00 (10 p.m.)
    if not (time(1, 0) <= hora_local < time(22, 0)):
        return JsonResponse({"ok": False, "mensaje": "Registro fuera de horario (5:00 a 22:00)."})

    # Último registro abierto del usuario
    reg = Asistencia.objects.filter(
        id_usuario=usuario,
        fecha_salida__isnull=True
    ).order_by('-fecha_entrada').first()

    # Si tiene un registro sin salida de días anteriores, cerrarlo como pendiente
    if reg and reg.fecha_entrada.date() < hoy:
        cierre_prev = datetime.combine(reg.fecha_entrada.date(), time(22, 0))
        if timezone.is_naive(cierre_prev):
            cierre_prev = timezone.make_aware(cierre_prev, timezone.get_current_timezone())
        reg.fecha_salida = cierre_prev
        reg.estado = "Pendiente"
        reg.save(update_fields=["fecha_salida", "estado"])
        reg = None

    # Evita duplicar si acaba de marcar hace pocos segundos
    if reg and (ahora - reg.fecha_entrada) < timedelta(seconds=30):
        mensaje_asistencia = "Marca ya registrada hace segundos"
    else:
        if reg and reg.fecha_entrada.date() == hoy:
            # cerrar salida
            reg.fecha_salida = ahora
            reg.estado = "Salida"
            reg.save(update_fields=["fecha_salida", "estado"])
            mensaje_asistencia = "Salida registrada"
        else:
            # crear nueva entrada
            reg = Asistencia.objects.create(
                id_usuario=usuario,
                rol=(usuario.groups.first().name if usuario.groups.exists() else ""),
                fecha_entrada=ahora,
                fecha_salida=None,
                estado="Entrada"
            )
            mensaje_asistencia = "Entrada registrada"

    nombre = f"{usuario.first_name} {usuario.last_name}".strip() or usuario.username or f"ID {usuario.id}"
    mensaje_full = f"Asistencia validada. La asistencia del usuario {nombre} ha sido registrada correctamente."

    return JsonResponse({
        "ok": True,
        "usuario": nombre,
        "asistencia": mensaje_asistencia,
        "mensaje": mensaje_full,
        "entrada": reg.fecha_entrada,
        "salida": reg.fecha_salida,
    })

@login_required(login_url='login')
def CambiarPasswordCliente(request):
    """Permite al cliente cambiar su contraseña"""
    if request.method == 'POST':
        password_actual = request.POST.get('password_actual')
        password_nueva = request.POST.get('password_nueva')
        password_confirmar = request.POST.get('password_confirmar')
        
        # Verificar contraseña actual
        if not request.user.check_password(password_actual):
            messages.error(request, 'La contraseña actual es incorrecta')
            return redirect('Perfil')
        
        # Verificar que las nuevas coincidan
        if password_nueva != password_confirmar:
            messages.error(request, 'Las contraseñas nuevas no coinciden')
            return redirect('Perfil')
        
        # Verificar longitud mínima
        if len(password_nueva) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            return redirect('Perfil')
        
        # Cambiar contraseña
        request.user.set_password(password_nueva)
        request.user.save()
        
        # Mantener la sesión activa
        update_session_auth_hash(request, request.user)
        
        messages.success(request, '¡Contraseña actualizada exitosamente!')
        return redirect('Perfil')
    
    return redirect('Perfil')


@login_required(login_url='login')
def DetalleRutina(request, id):
    """Ver detalle de una rutina con sus ejercicios"""
    rutina = get_object_or_404(Rutina, Id_rutina=id, Estado='Activo')
    ejercicios = rutina.ejercicios.all().order_by('Orden')
    
    context = {
        'rutina': rutina,
        'ejercicios': ejercicios,
    }
    
    return render(request, 'templates_perfil/detalle_rutina.html', context)