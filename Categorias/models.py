from django.db import models

class categoria (models.Model):

    Id_categoria= models.AutoField(primary_key=True, db_column='Id_categoria')
    Nombre= models.CharField(max_length=50, db_column='Nombre') 
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

    class Meta: 
        db_table= 'categoria' 
        managed= False 

    def __str__(self): 
        return f"Nombre{self.Nombre} - Estado{self.Estado}"
