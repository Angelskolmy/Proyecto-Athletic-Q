from django import forms  
from .models import Salidas_Entradas 
from .models import producto 

class Form_EntSal(forms.ModelForm): 

    class Meta: 
        model=Salidas_Entradas 
        fields=['Tipo_Cambio','Precio_Afectado','Cambio_precio','Stock_Afectado','Descripcion_EntSal'] 

        widgets={

            'Tipo_Cambio' : forms.Select(attrs={
                'Class' : 'form-select',
                'Placeholder' : 'Tipo de Cambio al producto',
            }), 

            'Precio_Afectado' : forms.NumberInput(attrs={
                'Class' : 'form-control numero', 
                'Placeholder' : 'Afectar precio del producto',
            }), 

            'Cambio_precio' : forms.Select(attrs={
                'Class' : 'form-select', 
                'Placeholder' : 'Cambio de precio del producto',
            }), 

            'Stock_Afectado' : forms.NumberInput(attrs={
                'Class' : 'form-control numero',
                'Placeholdder' : 'Afectar stock del producto',
            }), 

            'Descripcion_EntSal': forms.Textarea(attrs={
                'Class' : 'form-control', 
                'Placeholder' : 'Descripcion de la entrada/salida',
            }),
        }