from django.contrib.auth.models import AbstractUser
from django.db import models

class User_Gym(models.Model):
    class Meta:
        permissions = [
            ("usariogym", "Puede acceder a la vista usuariogym")
        ]


class User_Empleados(AbstractUser):

    id = models.AutoField(primary_key=True, db_column='id')

    password = models.CharField(max_length=128, db_column='password')

    last_login = models.DateTimeField(null=True, blank=True, db_column='last_login')

    is_superuser = models.BooleanField(default=False, db_column='is_superuser')

    username = models.CharField(max_length=150, unique=True, db_column='username')

    first_name = models.CharField(max_length=150, blank=True, db_column='first_name')

    last_name = models.CharField(max_length=150, blank=True, db_column='last_name')

    email = models.EmailField(max_length=254, blank=True, db_column='email')

    is_staff = models.BooleanField(default=False, db_column='is_staff')

    is_active = models.BooleanField(default=True, db_column='is_active')

    date_joined = models.DateTimeField(auto_now_add=True, db_column='date_joined')

    Eps = models.CharField(max_length=50, null=True, blank=True, db_column='Eps')

    Sexo_choice = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
    ]
    Sexo = models.CharField(
        choices=Sexo_choice,
        max_length=20,
        null=True,
        blank=True,
        db_column='Sexo'
    )

    Cedula = models.IntegerField(unique=True, null=True, blank=True, db_column='Cedula')

    empleados_img = models.CharField(max_length=100, null=True, blank=True, db_column='empleados_img')

    Huella_id = models.IntegerField(null=True, blank=True, db_column='Huella_id')

    class Meta:
        db_table = 'Empleados_user_empleados'


    def _str_(self): 
        return f" id {self.id} - password {self.password} - last_login {self.last_login} - is_superuser {self.is_superuser} - username {self.username} - first_name {self.first_name} - last_name {self.last_name} - email {self.email} - is_staff{self.is_staff} - is_active {self.is_active} - date_joined {self.date_joined} - EPS {self.Eps} - Sexo {self.Sexo} - Cedula {self.Cedula} - empleados_img {self.empleados_img} - Huella_id {self.Huella_id}"