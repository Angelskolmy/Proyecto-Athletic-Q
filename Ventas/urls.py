from django.urls import path
from . import views

urlpatterns = [
    path('Ventas/', views.ListarVentas, name='Ventas'),
    path('Ventas/procesar/', views.ProcesarVenta, name='procesar_venta'),
    path('Ventas/detalle/<int:id>/', views.DetalleVenta, name='detalle_venta'),
    path('Ventas/edit/<int:id>/', views.EditarVenta, name='editar_venta'),
    path('Ventas/actualizar/<int:id>/', views.ActualizarVenta, name='actualizar_venta'),
    
    # Exportar
    path('Ventas/exportar/excel/<int:id>/', views.ExportarVentaExcel, name='exportar_venta_excel'),
    path('Ventas/exportar/pdf/<int:id>/', views.ExportarVentaPDF, name='exportar_venta_pdf'),
]