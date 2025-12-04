from django.contrib import admin
from django.urls import path,include 
from Salidas_Entradas import views

urlpatterns = [ 

    path('EstSal/<int:Id_producto>/', views.listEst_Sal, name='EstSal'), 
    path('IngEstSal/<int:Id_producto>/', views.IngresarEntradaOSalida, name='IngEstSal'), 
    path('BUsqENsal/', views.BUscadorE, name='BUsqENsal')
    
]  