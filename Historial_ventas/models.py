from django.db import models
from Empleados.models import User_Empleados

class Historial_Ventas(models.Model): 

    id_registro= models.AutoField(primary_key=True, db_column='id_registro')
    fecha_venta= models.DateTimeField(auto_now_add=True, db_column='fecha_venta') 
    Monto= models.DecimalField(max_digits=10, decimal_places=2, db_column='Monto')  
    id_usuario= models.ForeignKey(User_Empleados, on_delete=models.CASCADE, db_column='id_usuario')  
    Metodo_pago_Choice=[ 

        ('Fisico', 'Fisico'), 
        ('Credito', 'Credito'),
        ('Debito', 'Debito'),
        ('PSE', 'PSE'),
        ('Nequi', 'Nequi'),
    ] 
    metodo_pago= models.CharField(
        max_length=30, 
        choices=Metodo_pago_Choice, 
        db_column='metodo_pago', 
        default=''
    )

    class Meta: 

        db_table='historial_ventas'
        managed=False  

    def __str__(self): 
        return f"id_registro{self.id_registro} - fecha_venta{self.fecha_venta} - Monto{self.Monto} - id_usuario{self.id_usuario} - metodo_pago{self.metodo_pago}"
