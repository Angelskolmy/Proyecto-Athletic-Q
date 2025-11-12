from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import TipoMembresia
from .forms import TipoMembresiaForm


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
        'tipo': tipo
    })
