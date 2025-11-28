from django.db import models
from Empleados.models import User_Empleados 
from django.utils import timezone

class Historial_usuario(models.Model): 

    Id_historial= models.AutoField(primary_key=True, db_column='Id_historial') 
    Fecha_y_hora= models.DateField( null=True,db_column='Fecha_y_hora')
    id_usuario= models.ForeignKey(User_Empleados, on_delete=models.CASCADE, db_column='id_usuario') 
    TIpo_Movimiento_CHOICES=[
        ('ingresar','ingresar'),
        ('eliminar','eliminar'),
        ('editar','editar'),
    ]
    TIpo_Movimiento= models.CharField(

        choices=TIpo_Movimiento_CHOICES, 
        db_column='TIpo_Movimiento', 
        max_length=14,
        default='',
        null=True
    ) 
    Modulo_CHOICES= [
        ('usuarios','usuarios'),
        ('ventas','ventas'),
        ('productos','productos'),
        ('categorías','categorías'),
        ('membresías','membresías'), 
        ('Tipo_Membresias','Tipo_Membresias'),
    ] 
    Modulo= models.CharField(

        choices=Modulo_CHOICES, 
        db_column='Modulo', 
        max_length=20, 
        default='',
        null=True
    ) 
    Nombre_Objeto= models.CharField(max_length=50, db_column='Nombre_Objeto') 
    Id_Objeto= models.IntegerField( db_column='Id_Objeto') 


    class Meta: 

        db_table='historial_usuario' 
        managed= False
    
    def __str__(self): 

        return f"Id_historial{self.Id_historial} - Fecha_y_hora{self.Fecha_y_hora} - id_usuario{self.id_usuario} - TIpo_Movimiento{self.TIpo_Movimiento} - Modulo{self.Modulo} - Nombre_Objeto{self.Nombre_Objeto} - Id_Objeto{self.Id_Objeto}"