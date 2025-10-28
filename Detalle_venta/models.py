from django.db import models
from Productos.models import producto 
from Ventas.models import Venta

class Detalle_Venta (models.Model): 

    Id_detalle= models.AutoField(primary_key=True, db_column='Id_detalle') 
    Id_venta= models.ForeignKey(Venta, on_delete=models.CASCADE,db_column='Id_venta') 
    Id_producto= models.ForeignKey(producto, on_delete=models.CASCADE, db_column='Id_producto') 
    Pago_Choice=[
        ('PSE','PSE'),
        ('Efectivo','Efectivo'),
        ('Nequ','Nequ'),
    ] 
    Tipo_Pago= models.CharField(
        max_length=50, 
        default='',
        choices=Pago_Choice, 
        db_column='Tipo_Pago'
    ) 
    Cantidad= models.IntegerField()
    Subtotal= models.DecimalField(max_digits=10, decimal_places=2, db_column='Subtotal') 
    Total= models.DecimalField(max_digits=10, decimal_places=2, db_column='Total') 

    class Meta: 

        db_table='detalle_venta' 
        managed=False 

    def __str__(self): 
        return f"Id_detalle{self.Id_detalle} -Id_venta{self.Id_venta} - Id_producto{self.Id_producto} - Tipo_Pago{self.Tipo_Pago} - Cantidad{self.Cantidad} - Subtotal{self.Subtotal} - Total{self.Total}"

