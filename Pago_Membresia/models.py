from django.db import models
from Membresias.models import Membresia

class Pago_membresia(models.Model): 

    Id_pago= models.AutoField(primary_key=True, db_column='Id_pago') 
    Id_membresia= models.ForeignKey(Membresia, on_delete=models.CASCADE, db_column='Id_membresia') 
    Fecha_pago= models.DateField( db_column='Fecha_pago') 
    Monto= models.DecimalField(max_digits=10, decimal_places=2, db_column='Monto')

    class Meta: 
        db_table='pago_membresia'
        managed=False  
    
    def __str__(self): 
        return f"Id_pago{self.Id_pago} - Id_membresia{self.Id_membresia} - Fecha_pago{self.Fecha_pago} - Monto{self.Monto}"

