from django.db import models
from Productos.models import producto 
from Ventas.models import Venta


class Detalle_Venta(models.Model):
    Id_detalle = models.AutoField(
        primary_key=True,
        db_column='Id_detalle'
    )

    Id_venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        db_column='Id_venta',
        null=True,
        blank=True,
    )

    Id_producto = models.ForeignKey(
        producto,
        on_delete=models.CASCADE,
        db_column='Id_producto',
        null=True,
        blank=True,
    )

    Pago_Choice = [
        ('Efectivo', 'Efectivo'),
        ('Credito', 'Crédito'),
        ('Debito', 'Débito'),
        ('PSE', 'PSE'),
        ('Nequi', 'Nequi'),
    ]

    Tipo_Pago = models.CharField(
        max_length=50,
        default='Efectivo',
        choices=Pago_Choice,
        db_column='Tipo_Pago'
    )

    Cantidad = models.IntegerField(
        db_column='Cantidad'
    )

    Subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column='Subtotal'
    )

    Total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column='Total'
    )

    class Meta:
        db_table = 'detalle_venta'
        managed = False

    def _str_(self):
        return (
            f"Id_detalle {self.Id_detalle} - Id_venta {self.Id_venta} - "
            f"Id_producto {self.Id_producto} - Tipo_Pago {self.Tipo_Pago} - "
            f"Cantidad {self.Cantidad} - Subtotal {self.Subtotal} - Total {self.Total}"
        )