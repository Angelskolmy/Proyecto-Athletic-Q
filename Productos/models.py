from django.db import models 
from Categorias.models import categoria

class producto(models.Model): 
    
    Id_producto= models.AutoField(primary_key=True, db_column='Id_producto')
    Catego_Id= models.ForeignKey(categoria, on_delete=models.CASCADE, db_column='Catego_Id')
    Nombre= models.CharField(max_length=100,db_column='Nombre')
    Descripcion= models.TextField(db_column='Descripcion')  
    Stock= models.IntegerField(db_column='Stock')
    Precio_de_compra= models.DecimalField(max_digits=10, decimal_places=2, db_column='Precio_de_compra')  
    Precio_de_venta= models.DecimalField(max_digits=10, decimal_places=2, db_column='Precio_de_venta')  
    Estado_Choice=[
        ('Activo','Activo'),
        ('Inactivo','Inactivo'),
    ]
    Estado= models.CharField(

        choices=Estado_Choice, 
        default='Activo', 
        max_length=8, 
        db_column='Estado'
    )  
    prod_imagen= models.ImageField(upload_to='productos_media/',max_length=100, db_column='prod_imagen')

    class Meta: 
        db_table='producto'
        managed= False 

    def __str__(self): 
        return f"Nombre{self.Nombre} - Descripcion{self.Descripcion} - Stock{self.Stock} - Pre_Compra{self.Precio_de_compra} - Pre_Venta{self.Precio_de_venta} - prod_imagen{self.prod_imagen}"