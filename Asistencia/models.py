from django.db import models
from Empleados.models import User_Empleados

class asistencia(models.Model): 

    Id_asistencia= models.AutoField(primary_key=True, db_column='Id_asistencia')  
    Fecha_Hora= models.DateTimeField(auto_now_add=True, db_column='Fecha_Hora') 
    id_usuario= models.ForeignKey(User_Empleados, on_delete=models.CASCADE, db_column='id_usuario') 

    class Meta: 
        db_table='asistencia'
        managed= False 
        
    def __str__(self):
        return f"Id_asistencia{self.Id_asistencia} - Fecha_Hora{self.Fecha_Hora} - id_usuario{self.id_usuario}"