from django.db import models

class Rutina(models.Model):
    Id_rutina = models.AutoField(primary_key=True, db_column='Id_rutina')
    Nombre = models.CharField(max_length=100, db_column='Nombre')
    Descripcion = models.TextField(db_column='Descripcion', null=True, blank=True)
    
    NIVEL_CHOICES = [
        ('Principiante', 'Principiante'),
        ('Intermedio', 'Intermedio'),
        ('Avanzado', 'Avanzado'),
    ]
    Nivel = models.CharField(
        max_length=20, 
        choices=NIVEL_CHOICES, 
        default='Principiante',
        db_column='Nivel'
    )
    
    CATEGORIA_CHOICES = [
        ('Pecho', 'Pecho'),
        ('Espalda', 'Espalda'),
        ('Piernas', 'Piernas'),
        ('Hombros', 'Hombros'),
        ('Brazos', 'Brazos'),
        ('Abdomen', 'Abdomen'),
        ('Cardio', 'Cardio'),
        ('Full Body', 'Full Body'),
    ]
    Categoria = models.CharField(
        max_length=20, 
        choices=CATEGORIA_CHOICES,
        db_column='Categoria'
    )
    
    Duracion_minutos = models.IntegerField(db_column='Duracion_minutos', default=30)
    Calorias_estimadas = models.IntegerField(db_column='Calorias_estimadas', null=True, blank=True)
    
    rutina_img = models.ImageField(
        upload_to='rutinas/',
        max_length=100,
        blank=True,
        null=True,
        db_column='rutina_img'
    )
    
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    Estado = models.CharField(
        max_length=10, 
        choices=ESTADO_CHOICES, 
        default='Activo',
        db_column='Estado'
    )
    
    Fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='Fecha_creacion')

    class Meta:
        db_table = 'rutina'
        managed = True
        verbose_name = 'Rutina'
        verbose_name_plural = 'Rutinas'

    def __str__(self):
        return f"{self.Nombre} - {self.Categoria} ({self.Nivel})"


class Ejercicio(models.Model):
    Id_ejercicio = models.AutoField(primary_key=True, db_column='Id_ejercicio')
    Id_rutina = models.ForeignKey(
        Rutina, 
        on_delete=models.CASCADE, 
        related_name='ejercicios',
        db_column='Id_rutina'
    )
    Nombre = models.CharField(max_length=100, db_column='Nombre')
    Descripcion = models.TextField(db_column='Descripcion', null=True, blank=True)
    Series = models.IntegerField(db_column='Series', default=3)
    Repeticiones = models.CharField(max_length=50, db_column='Repeticiones', default='10-12')
    Descanso_segundos = models.IntegerField(db_column='Descanso_segundos', default=60)
    Orden = models.IntegerField(db_column='Orden', default=1)
    
    ejercicio_img = models.ImageField(
        upload_to='ejercicios/',
        max_length=100,
        blank=True,
        null=True,
        db_column='ejercicio_img'
    )

    class Meta:
        db_table = 'ejercicio'
        managed = True
        ordering = ['Orden']

    def __str__(self):
        return f"{self.Nombre} - {self.Series}x{self.Repeticiones}"