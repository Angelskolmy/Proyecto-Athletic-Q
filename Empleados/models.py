from django.db import models
from django.contrib.auth.models import AbstractUser


class User_Gym(models.Model):
    """
    Modelo usado solo para declarar permisos personalizados.
    """
    class Meta:
        permissions = [
            ("usuariogym", "Puede acceder a la vista usuariogym"),
        ]

    def _str_(self):
        return "Permisos de usuario de gimnasio"


class User_Empleados(AbstractUser):
    Eps = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_column='Eps'
    )

    SEXO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
    ]
    Sexo = models.CharField(
        choices=SEXO_CHOICES,
        max_length=20,
        null=True,
        blank=True,
        db_column='Sexo'
    )
    
    TIPO_DOC_CHOICES = [
        ('CC', 'Cédula de ciudadanía'),
        ('TI', 'Tarjeta de identidad'),
        ('CE', 'Cédula de extranjería'),
        ('PA', 'Pasaporte'),
    ]
    
    TipoDocumento = models.CharField(
        max_length=3,
        choices=TIPO_DOC_CHOICES,
        null=True,
        blank=True,
        db_column='TipoDocumento'
    )

    Cedula = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
        db_column='Cedula'
    )

    empleados_img = models.ImageField(
        upload_to='usuarios/',
        max_length=100,
        null=True,
        blank=True,
        db_column='empleados_img'
    )

    Direccion = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_column='Direccion'
    )

    Celular = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        db_column='Celular'
    )

    class Meta:
        managed = False
        db_table = 'Empleados_user_empleados'
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def _str_(self):
        nombre = f"{self.first_name} {self.last_name}".strip()
        if nombre:
            return f"{self.username} - {nombre}"
        return self.username