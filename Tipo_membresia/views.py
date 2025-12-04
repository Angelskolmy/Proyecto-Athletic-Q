from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import TipoMembresia
from .forms import TipoMembresiaForm 
from django.utils import timezone  
from Historial.models import Historial_usuario



@login_required(login_url='login')
@permission_required('Tipo_membresia.view_tipomembresia', login_url='login')
def listarTiposMembresia(request):
    tipos = TipoMembresia.objects.all().order_by('Duracion_meses')
    context = {'TiposMembresia': tipos}
    return render(request, 'templates_tipo_membresia/tipo_membresia.html', context)


@login_required(login_url='login')
@permission_required('Tipo_membresia.add_tipomembresia', login_url='TiposMembresia')
@transaction.atomic
def crearTipoMembresia(request):
    if request.method == 'POST':
        form = TipoMembresiaForm(request.POST, request.FILES)
        if form.is_valid():
            Roling3= form.save() 

            histuser4 = request.user
            histMod4 = 'Tipo_Membresias'
            histMovs4 = 'ingresar'
            histFech4 = timezone.now().date()             
            histNomb4 = Roling3.Nombre 
            histId4 = Roling3.Id_tipo_membresia

            Historial_usuario.objects.create(
                id_usuario= histuser4,
                TIpo_Movimiento= histMovs4,
                Modulo= histMod4,
                Nombre_Objeto= histNomb4,
                Id_Objeto= histId4,
                Fecha_y_hora= histFech4,
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
    
    if request.method == 'POST':
        form = TipoMembresiaForm(request.POST, request.FILES, instance=tipo)
        if form.is_valid():
            Roling4= form.save()  

            histuser5 = request.user
            histMod5 = 'Tipo_Membresias'
            histMovs5 = 'editar'
            histFech5 = timezone.now().date()             
            histNomb5 = Roling4.Nombre 
            histId5 = Roling4.Id_tipo_membresia

            Historial_usuario.objects.create(
                id_usuario= histuser5,
                TIpo_Movimiento= histMovs5,
                Modulo= histMod5,
                Nombre_Objeto= histNomb5,
                Id_Objeto= histId5,
                Fecha_y_hora= histFech5,
            )


            messages.success(request, 'Tipo de membresía actualizado exitosamente.')
            return redirect('TiposMembresia')
    else:
        form = TipoMembresiaForm(instance=tipo)
    
    return render(request, 'templates_tipo_membresia/editar_tipo_membresia.html', {
        'form': form,
        'tipo': tipo
    })
