from django.shortcuts import render, redirect
from .models import categoria 
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def listarCategorias (request): 
    if not request.user.has_perm('Categorias.view_categoria'):
        messages.warning(request, "No tienes permiso para acceder a esta sección.")
        return redirect('Perfil')  # URL de perfil
    
    AllCatego= categoria.objects.all() 
    Lister= { 'Categorias' : AllCatego}  
    return render (request, "templates_categoria/categorias.html", Lister)
