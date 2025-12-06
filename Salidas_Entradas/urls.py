from django.contrib import admin
from django.urls import path,include 
from Salidas_Entradas import views

urlpatterns = [ 

    path('EstSal/<int:Id_producto>/', views.ListarSalidasEntradas, name='EstSal'), 
    path('IngEstSal/<int:Id_producto>/', views.CrearSalidasEntradas, name='IngEstSal'), 
    path('BUsqENsal/', views.BuscadorSalidasEntradas, name='BUsqENsal')
    
]  