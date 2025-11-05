from django.shortcuts import render
from .models import Membresia
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def ListMebresias(request): 

    AllistMemb= Membresia.objects.all() 
    ContMemb= {'AllMebs':AllistMemb} 
    return render(request, 'templates_membresias/membresias.html' ,ContMemb)
