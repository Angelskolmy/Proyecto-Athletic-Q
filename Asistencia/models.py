from django.db import models
from django.utils import timezone
from Empleados.models import User_Empleados


class Asistencia(models.Model):
    id = models.BigAutoField(
        primary_key=True
    )

    id_usuario = models.ForeignKey(
        User_Empleados,
        on_delete=models.CASCADE,
        related_name="asistencias",
        db_column="id_usuario",
        null=True,
        blank=True,
    )

    rol = models.CharField(
        max_length=50,
        default="",
        blank=True
    )

    fecha_entrada = models.DateTimeField(
        default=timezone.now
    )

    fecha_salida = models.DateTimeField(
        null=True,
        blank=True
    )

    estado = models.CharField(
        max_length=30,
        default="",
        blank=True
    )

    class Meta:
        db_table = "Asistencia"
        ordering = ["-fecha_entrada"]
        managed = False

    def _str_(self):
        return f"{self.id_usuario} | {self.fecha_entrada} -> {self.fecha_salida or '—'}"