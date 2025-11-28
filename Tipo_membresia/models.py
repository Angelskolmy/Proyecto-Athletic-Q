from django.db import models

class TipoMembresia(models.Model):
    Id_tipo_membresia = models.AutoField(primary_key=True, db_column='Id_tipo_membresia')
    Nombre = models.CharField(max_length=100, db_column='Nombre', unique=True)
    DURACION_CHOICES = [
        (1, '1 Mes'),
        (3, '3 Meses'),
        (6, '6 Meses'),
        (12, '12 Meses (1 Año)'),
        (24, '24 Meses (2 Años)'),
    ]
    Duracion_meses = models.IntegerField(
        choices=DURACION_CHOICES,
        default=1,
        db_column='Duracion_meses'
    )
    Precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        db_column='Precio'
    )
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    Estado = models.CharField(
        max_length=8,
        choices=ESTADO_CHOICES,
        default='Activo',
        db_column='Estado'
    )
    tipo_membresia_img = models.ImageField(
        upload_to='tipos_membresia/',
        max_length=100,
        blank=True,
        null=True,
        db_column='tipo_membresia_img'
    )
    
    class Meta:
        db_table = 'tipo_membresia'
        managed = False
        verbose_name = 'Tipo de Membresía'
        verbose_name_plural = 'Tipos de Membresías'
    
    def str(self):
        return f" Id_tipo_membresia{self.Id_tipo_membresia} - Nombre:{self.Nombre} - Duracion:{self.Duracion_meses} meses - Precio:{self.Precio} - Estado:{self.Estado} - tipo_membresia_img{self.tipo_membresia_img}"