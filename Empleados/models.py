from django.contrib.auth.models import AbstractUser
from django.db import models

class User_Empleados(AbstractUser): 

    id= models.AutoField(primary_key=True, db_column='id', null=False) 
    password= models.CharField(max_length=128, null=False, db_column='password')
    last_login= models.DateTimeField(db_column='last_login') 
    is_superuser=models.BooleanField(null=False, db_column='is_superuser') 
    username= models.CharField(max_length=150, null=False, unique=True, db_column='username')
    first_name= models.CharField(max_length=150, null=False, db_column='first_name') 
    last_name= models.CharField(max_length=150, null=False, db_column='last_name') 
    email= models.CharField(max_length=250, null=False, db_column='email')  
    is_staff=models.BooleanField(null=False, db_column='is_staff') 
    is_active=models.BooleanField(null=False, db_column='is_active')
    date_joined= models.DateTimeField(null=False, db_column='date_joined')
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
    Huella_id= models.IntegerField(db_column='Huella_id')

    class Meta: 

        managed= True
        db_table= 'Empleados_user_empleados'

    def __str__(self): 
        return f" id {self.id} - password {self.password} - last_login {self.last_login} - is_superuser {self.is_superuser} - username {self.username} - first_name {self.first_name} - last_name {self.last_name} - email {self.email} - is_staff{self.is_staff} - is_active {self.is_active} - date_joined {self.date_joined} - EPS {self.Eps} - Sexo {self.Sexo} - Cedula {self.Cedula} - empleados_img {self.empleados_img} - Huella_id {self.Huella_id}" 