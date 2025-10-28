from django.shortcuts import render
from .models import Membresia

def ListMebresias(request): 

    AllistMemb= Membresia.objects.all() 
    ContMemb= {'AllMebs':AllistMemb} 
    return render(request, 'templates_membresias/membresias.html' ,ContMemb)
