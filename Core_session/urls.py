from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('recuperar/', views.recuperar_view, name='recuperar'),
    path('codigo/', views.codigo_view, name='codigo'),
    path('nueva/', views.nueva_view, name='nueva'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
]

