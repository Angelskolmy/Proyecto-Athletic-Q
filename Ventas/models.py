from django.db import models
from Empleados.models import User_Empleados


class Venta (models.Model):

    Id_venta= models.AutoField(primary_key=True, db_column='Id_venta') 
    Fecha= models.DateTimeField(auto_now_add=True, db_column='Fecha') 
    Total= models.DecimalField(max_digits=10, decimal_places=2, db_column='Total') 
    id_usuario= models.ForeignKey(User_Empleados, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta: 
        db_table='venta'
        managed=False 

    def __str__(self): 
        return f"Id_venta{self.Id_venta} - Fecha{self.Fecha} - Total{self.Total} id_usuario{self.id_usuario}"