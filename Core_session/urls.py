from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('correo/', views.enviar_codigo, name='correo'),
    path('codigo_recuperacion/', views.vista_codigo, name='codigo_recuperacion'),
    path('codigo/', views.validar_codigo, name='codigo'),
    path('invalidar-codigo/', views.invalidar_codigo, name='invalidar_codigo'),
    path('reenviar-codigo/', views.reenviar_codigo, name='reenviar_codigo'),
    path('contra_nueva/', views.vista_cambiar_contraseña, name='contra_nueva'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    
    # API para gráficos AJAX
    path('home/ajax/chart/<str:name>/', views.home_chart, name='home_chart'),
]