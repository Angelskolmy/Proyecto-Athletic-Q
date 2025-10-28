from django.db import models
from Empleados.models import User_Empleados

class Membresia(models.Model): 

    Id_membresia= models.AutoField(primary_key=True, db_column='Id_membresia') 
    Fecha_inicio= models.DateTimeField(auto_now_add=True,db_column='Fecha_inicio') 
    Fecha_fin= models.DateField(db_column='Fecha_fin')
    Estado_Choice=[
        ('Activo','Activo'),
        ('Inactivo','Inactivo'),
    ]
    Estado= models.CharField(

        choices=Estado_Choice, 
        default='Activo', 
        max_length=10, 
        db_column='Estado'
    )   
    id_usuario= models.ForeignKey(User_Empleados, on_delete=models.CASCADE, db_column='id_usuario')
    Duracion_meses= models.IntegerField( db_column='Duracion_meses')
    Precio= models.DecimalField(max_digits=10, decimal_places=2, db_column='Precio')  
    membresia_img= models.CharField(max_length=100, db_column='membresia_img')

    class Meta: 

        managed= False 
        db_table='membresia' 

    def __str__(self): 
        return f"Id_membresia{self.Id_membresia} - Fecha_inicio{self.Fecha_inicio} - Fecha_fin{self.Fecha_fin} - Estado{self.Estado} - id_usuario{self.id_usuario} - Duracion_meses{self.Duracion_meses} - Precio{self.Precio} - membresia_img{self.membresia_img}"