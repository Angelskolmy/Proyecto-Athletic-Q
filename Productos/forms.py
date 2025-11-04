from django import forms 
from .models import producto 

class ProductoForm(forms.ModelsFom): 
    
    class Meta: 
        model=producto
        fields=['','','','','','','']