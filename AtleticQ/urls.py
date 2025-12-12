from django.contrib import admin
from django.urls import path, include 
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('/login/'), name='root'),
    path('', include("Core_session.urls")),
    path('', include("Productos.urls")),
    path('', include("Categorias.urls")),
    path('', include("Asistencia.urls")),
    path('', include("Detalle_venta.urls")),
    path('', include("Empleados.urls")),
    path('', include("Historial.urls")),
    path('', include("Historial_ventas.urls")),
    path('', include("Membresias.urls")),
    path('', include('Tipo_membresia.urls')),
    path('', include("Ventas.urls")),
    path('', include("Salidas_Entradas.urls")),
]
handler403 = 'Core_session.views.error_403_view'
handler404 = 'Core_session.views.error_404_view'
handler500 = 'Core_session.views.error_500_view'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
