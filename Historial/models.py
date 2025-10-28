from django.db import models
from Empleados.models import User_Empleados

class Historial_usuario(models.Model): 

    Id_historial= models.AutoField(primary_key=True, db_column='Id_historial') 
    Descripcion= models.CharField(max_length=255, db_column='Descripcion')
    Fecha_y_hora= models.DateTimeField(auto_now_add=True, db_column='Fecha_y_hora')
    id_usuario= models.ForeignKey(User_Empleados, on_delete=models.CASCADE, db_column='id_usuario') 

    class Meta: 

        db_table='historial_usuario' 
        managed= False
    
    def __str__(self): 

        return f"Id_historial{self.Id_historial} - Descripcion{self.Descripcion} - Fecha_y_hora{self.Fecha_y_hora} - id_usuario{self.id_usuario}"