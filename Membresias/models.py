from django.db import models
from Empleados.models import User_Empleados 
from Tipo_membresia.models import TipoMembresia

class Membresia(models.Model): 

    Id_membresia = models.AutoField(primary_key=True, db_column='Id_membresia') 
    Fecha_inicio = models.DateTimeField(auto_now_add=True, db_column='Fecha_inicio') 
    Fecha_fin = models.DateField(db_column='Fecha_fin')
    
    Estado_Choice = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    Estado = models.CharField(
        choices=Estado_Choice, 
        default='Activo', 
        max_length=10, 
        db_column='Estado'
    )   
    
    id_usuario = models.ForeignKey(
        User_Empleados, 
        on_delete=models.CASCADE, 
        db_column='id_usuario'
    )  
    
    membresia_img = models.ImageField(
        upload_to='membresias/',
        max_length=100,
        blank=True,
        null=True,
        db_column='membresia_img'
    )
    
    # Llave foránea a Tipo de Membresía
    For_Id_tipo_membresia = models.ForeignKey(
        TipoMembresia, 
        on_delete=models.CASCADE, 
        db_column='For_Id_tipo_membresia'
    )
    
    class Meta: 
        managed = False 
        db_table = 'membresia' 

    def __str__(self): 
        return f"Membresía #{self.Id_membresia} - {self.id_usuario.first_name} {self.id_usuario.last_name} - {self.For_Id_tipo_membresia.Nombre}"