from django.db import models
from Productos.models import producto


class Salidas_Entradas (models.Model): 

    Id_SalEnt= models.AutoField(primary_key=True, db_column='Id_SalEnt') 
    Id_ProAsoc= models.ForeignKey(producto, on_delete=models.CASCADE, db_column='Id_ProAsoc') 
    EntSal_CHOICES=[
        ('Entrada','Entrada'),
        ('Salida','Salida'),
    ]  
    MovPrecio_CHOICES=[
       ('Incrementar','Incrementar'),
       ('Bajar','Bajar'),
    ]

    Tipo_Cambio= models.CharField( 

        choices= EntSal_CHOICES, 
        default= '', 
        max_length=30, 
        db_column='Tipo_Cambio', 
        null=True,
    ) 

    Cambio_precio= models.CharField(
       
       choices= MovPrecio_CHOICES, 
       default= '', 
       max_length=30, 
       db_column='Cambio_precio', 
       null=True
    )
    Precio_Afectado= models.DecimalField(db_column='Precio_Afectado',  decimal_places=2, max_digits=10, null=True) 
    Stock_Afectado= models.IntegerField(db_column='Stock_Afectado', null=True) 
    Fecha_cambio= models.DateField(db_column='Fecha_cambio', null=True) 
    Descripcion_EntSal= models.TextField(db_column='Descripcion_EntSal', null=True) 

    class Meta: 

        db_table='Salidas_Entradas'
        managed=False 

    
    def __str__(self): 
      return f"Id_SalEnt{self.Id_SalEnt} - Id_ProAsoc{self.Id_ProAsoc} - Tipo_Cambio{self.Tipo_Cambio} - Precio_Afectado{self.Precio_Afectado} - Stock_Afectado{self.Stock_Afectado} - Fecha_cambio{self.Fecha_cambio} - Descripcion{self.Descripcion}"