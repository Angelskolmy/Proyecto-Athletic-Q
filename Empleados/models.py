from django.contrib.auth.models import AbstractUser
from django.db import models

class User_Empleados(AbstractUser):
    Eps= models.CharField(max_length=50, null=True, db_column='Eps')  
    Sexo_choice=[
        ('Masculino','Masculino'),
        ('Femenino','Femenino')
    ] 
    Sexo= models.CharField(
        choices=Sexo_choice,
        default='', 
        max_length=20, 
        null=True,
        db_column='Sexo'
    ) 
    Cedula= models.IntegerField(unique=True, null=True, db_column='Cedula')  
    empleados_img= models.CharField(max_length=100 ,null=True, db_column='empleados_img') 

    class Meta: 

        managed= False 
        db_table= 'Empleados_user_empleados'

    def __str__(self): 
        return f"EPS{self.Eps} - Sexo{self.Sexo} - Cedulo{self.Cedula} - empleados_img{self.empleados_img}"