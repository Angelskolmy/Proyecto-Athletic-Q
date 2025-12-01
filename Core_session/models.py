from django.contrib.auth.models import AbstractUser
from django.db import models

class asistencias(models.Model):
    class Meta:
        permissions = [
            ("usariogym", "Puede acceder a la vista usuariogym")
        ]