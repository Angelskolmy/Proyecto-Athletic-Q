from django.contrib.auth.models import AbstractUser
from django.db import models


class User_Gym(models.Model):
    """
    Modelo usado solo para declarar permisos personalizados.
    """
    class Meta:
        permissions = [
            ("usuariogym", "Puede acceder a la vista usuariogym"),
        ]

    def __str__(self):
        return "Permisos de usuario de gimnasio"


class User_Empleados(AbstractUser):
    # Campos extra respecto a AbstractUser

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

    # Mejor CharField que BinaryField para una dirección
    Direccion = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_column='Direccion'
    )

    # Mejor CharField que IntegerField para teléfonos (pueden tener +, -, espacios)
    Celular = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        db_column='Celular'
    )

    class Meta:
        managed = True
        db_table = 'Empleados_user_empleados'
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self):
        nombre = f"{self.first_name} {self.last_name}".strip()
        if nombre:
            return f"{self.username} - {nombre}"
        return self.username
