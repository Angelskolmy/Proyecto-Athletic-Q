from django.shortcuts import render
from .models import categoria 

def listarCategorias (request): 

    AllCatego= categoria.objects.all() 
    Lister= { 'Categorias' : AllCatego}  
    return render (request, "templates_categoria/categorias.html", Lister)
