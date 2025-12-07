from django.db import models
from Empleados.models import User_Empleados

class HuellaCaptura(models.Model):
    id_usuario = models.ForeignKey(
        User_Empleados,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        null=True,
        blank=True
    )

    template = models.TextField(
        db_column='template'
    )

    creado_en = models.DateTimeField(
        auto_now_add=True,
        db_column='Fecha_creacion'
    )

    class Meta:
        managed = False
        db_table = "huella_capturada"

    def _str_(self):
        return f"{self.id_usuario} - {self.creado_en}"