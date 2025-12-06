from django.shortcuts import render, redirect
from .models import producto
from .models import Salidas_Entradas
from .forms import Form_EntSal
from Historial.models import Historial_usuario
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from urllib.parse import urlencode


@login_required(login_url='login')
@permission_required('Salidas_Entradas.Salidas_Entradas', login_url='login')
def ListarSalidasEntradas(request, Id_producto):
    # detalle objeto, y listar tabla
    Detalleobj = producto.objects.get(Id_producto=Id_producto)
    table_primary = Salidas_Entradas.objects.filter(Id_ProAsoc=Id_producto).order_by('Id_ProAsoc')

    # cards consultas
    stadProd1 = Detalleobj.Stock * Detalleobj.Precio_de_venta
    stadProd2 = Salidas_Entradas.objects.filter(Id_ProAsoc=Id_producto, Tipo_Cambio='Salida').count()

    # paginacion
    Enclave = Paginator(table_primary, 6)
    Page_number = request.GET.get('page')
    Page_obj = Enclave.get_page(Page_number)

    Aquelarre = {
        'CardObjeto': [Detalleobj],
        'Entradas_Salidas': Page_obj,
        'Stock_Total': stadProd1,
        'Total_Salidas': stadProd2,
        'Id_producto': Id_producto,
    }

    return render(request, 'templates_salidas_entradas/salida_entrada.html', Aquelarre)


def CrearSalidasEntradas(request, Id_producto):
    ListProd = producto.objects.get(Id_producto=Id_producto)

    if request.method == "POST":
        runkerno = Form_EntSal(request.POST)

        if runkerno.is_valid():
            datos = runkerno.cleaned_data

            # --- STOCK ---
            if datos['Tipo_Cambio'] == 'Entrada':
                ListProd.Stock += datos['Stock_Afectado']
            elif datos['Tipo_Cambio'] == 'Salida':
                ListProd.Stock -= datos['Stock_Afectado']

            # --- PRECIO ---
            if datos['Cambio_precio'] == 'Incrementar':
                ListProd.Precio_de_venta += datos['Precio_Afectado']
            elif datos['Cambio_precio'] == 'Bajar':
                ListProd.Precio_de_venta -= datos['Precio_Afectado']

            with transaction.atomic():
                ListProd.save()
                Moves = runkerno.save(commit=False)
                Moves.Id_ProAsoc = ListProd
                Moves.Fecha_cambio = timezone.now().date()
                Moves.save()

            # GUARDAR MOVIMIENTO
            Historial_usuario.objects.create(
                id_usuario=request.user,
                TIpo_Movimiento="editar",
                Modulo="productos",
                Nombre_Objeto=ListProd.Nombre,
                Id_Objeto=ListProd.Id_producto,
                Fecha_y_hora=timezone.now().date()
            )

            return redirect('EstSal', Id_producto)

    else:
        runkerno = Form_EntSal()

    cifrer = {
        'runkerno': runkerno,
        'Id_producto': Id_producto,
    }

    return render(request, 'templates_salidas_entradas/ingresar_salida_entrada.html', cifrer)


def BuscadorSalidasEntradas(request):
    Fecha = request.GET.get('Fecha')
    Id_producto = request.GET.get('Id_producto')
    Cambio_precio = request.GET.get('Cambio_precio')

    if not ([Fecha, Cambio_precio]):
        return redirect('Producto')

    if Fecha:
        sqlBUsq44 = '''
            SELECT producto.*, Salidas_Entradas.* 
            FROM Salidas_Entradas 
            JOIN producto ON Salidas_Entradas.Id_ProAsoc = producto.Id_producto 
            WHERE Salidas_Entradas.Fecha_cambio = %s 
            AND Salidas_Entradas.Id_ProAsoc = %s
        '''
        busqRaw = Salidas_Entradas.objects.raw(sqlBUsq44, [Fecha, Id_producto])

    if Cambio_precio:
        sqlBUsq44 = '''
            SELECT producto.*, Salidas_Entradas.* 
            FROM Salidas_Entradas 
            JOIN producto ON Salidas_Entradas.Id_ProAsoc = producto.Id_producto 
            WHERE Salidas_Entradas.Cambio_precio = %s 
            AND Salidas_Entradas.Id_ProAsoc = %s
        '''
        busqRaw = Salidas_Entradas.objects.raw(sqlBUsq44, [Cambio_precio, Id_producto])

    if Fecha and Cambio_precio:
        sqlBUsq44 = '''
            SELECT producto.*, Salidas_Entradas.* 
            FROM Salidas_Entradas 
            JOIN producto ON Salidas_Entradas.Id_ProAsoc = producto.Id_producto 
            WHERE Salidas_Entradas.Fecha_cambio = %s 
            AND Salidas_Entradas.Cambio_precio = %s 
            AND Salidas_Entradas.Id_ProAsoc = %s
        '''
        busqRaw = Salidas_Entradas.objects.raw(sqlBUsq44, [Fecha, Cambio_precio, Id_producto])

    Conversor = list(busqRaw)
    Conclave = Paginator(Conversor, 6)
    Page_number = request.GET.get('page')
    Page_obj = Conclave.get_page(Page_number)

    params = {k: v for k, v in request.GET.items() if k != 'page' and v != ''}
    querystring = '&' + urlencode(params) if params else ''

    Detalleobj2 = producto.objects.get(Id_producto=Id_producto)
    stadProd1 = Detalleobj2.Stock * Detalleobj2.Precio_de_venta
    stadProd2 = Salidas_Entradas.objects.filter(Id_ProAsoc=Id_producto, Tipo_Cambio='Salida').count()

    Aquelarre2 = {
        'CardObjeto': [Detalleobj2],
        'Entradas_moebius22': Page_obj,
        'Stock_Total': stadProd1,
        'Total_Salidas': stadProd2,
        'Id_producto': Id_producto,
        'querystring': querystring,
    }

    return render(request, 'templates_salidas_entradas/salida_entrada.html', Aquelarre2)
