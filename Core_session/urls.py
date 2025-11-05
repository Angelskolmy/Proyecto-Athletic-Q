from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('recuperar/', views.recuperar1_view, name='recuperar1'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
]

