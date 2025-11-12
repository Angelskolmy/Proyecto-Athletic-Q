from django.contrib import admin
from django.urls import path, include 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("Core_session.urls")),
    path('', include("Productos.urls")),
    path('', include("Categorias.urls")),
    path('', include("Asistencia.urls")),
    path('', include("Detalle_venta.urls")),
    path('', include("Empleados.urls")),
    path('', include("Historial.urls")),
    path('', include("Historial_ventas.urls")),
    path('', include("Membresias.urls")),
    path('TiposMembresia/', include('Tipo_membresia.urls')),
    path('', include("Pago_Membresia.urls")),
    path('', include("Ventas.urls")),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)