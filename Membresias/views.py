from django.shortcuts import render, get_object_or_404, redirect
from .models import Membresia
from .form import MembresiaForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import timedelta

@login_required(login_url='login')
def ListMebresias(request): 

    AllistMemb= Membresia.objects.all() 
    ContMemb= {'AllMebs':AllistMemb} 
    return render(request, 'templates_membresias/membresias.html' ,ContMemb)

@permission_required('Membresias.change_membresia', login_url='Membresias')
def EditarMembresia(request, id):
    membresia = get_object_or_404(Membresia, Id_membresia=id)
    
    if request.method == 'POST':
        form = MembresiaForm(request.POST, instance=membresia)
        if form.is_valid():
            try:
                membresia = form.save(commit=False)
                
                # Recalcular fecha fin si cambió la duración
                if membresia.Duracion_meses:
                    fecha_inicio = membresia.Fecha_inicio.date() if hasattr(membresia.Fecha_inicio, 'date') else membresia.Fecha_inicio
                    membresia.Fecha_fin = fecha_inicio + timedelta(days=30 * membresia.Duracion_meses)
                
                membresia.save()
                
                messages.success(request, 'Membresía actualizada exitosamente')
                return redirect('Membresias')
                
            except Exception as e:
                messages.error(request, f'Error al actualizar la membresía: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = MembresiaForm(instance=membresia)

    context = {
        'form': form,
        'membresia': membresia,
    }
    
    return render(request, 'templates_membresias/editar_membresias.html', context)