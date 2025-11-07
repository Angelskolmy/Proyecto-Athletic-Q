from django.contrib import admin
from django.urls import path, include

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
    path('', include("Pago_Membresia.urls")),
    path('', include("Ventas.urls")),  
]