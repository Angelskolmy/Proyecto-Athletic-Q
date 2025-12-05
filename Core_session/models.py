from Empleados.models import User_Empleados
from django.db import models

class HuellaCaptura(models.Model):
    id_usuario = models.ForeignKey(
        User_Empleados,
        on_delete=models.CASCADE,
        db_column='id_usuario',
        null=True, blank=True  # deja True para migrar sin defaults
    )
    template = models.TextField(db_column='template')
    creado_en = models.DateTimeField(auto_now_add=True, db_column='Fecha_creacion')

    class Meta:
        db_table = "huella_capturada"