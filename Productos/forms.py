from django import forms 
from .models import producto 
from .models import categoria

class ProductoForm(forms.ModelForm): 
    
    class Meta: 
        model=producto
        fields=['Catego_Id','Nombre','Descripcion','Stock','Precio_de_compra','Precio_de_venta','prod_imagen','Estado']

        widgets={

            'Nombre': forms.TextInput(attrs={
                'Class':'form-control',
                'Placeholder':'Nombre',
            }), 
            
            'Catego_Id' : forms.Select(attrs={
                'Class': 'form-select', 
                'Placeholder':'Seleccione',
            }), 

            'Descripcion': forms.Textarea(attrs={
                'Class': 'form-control', 
                'Placeholder' : '', 
                'rows' : 3, 
            }),

            'Stock':forms.NumberInput(attrs={
                'Class': 'form-control', 
                'Placeholder': '',
                'min':'0',
            }), 

            'Precio_de_compra': forms.NumberInput(attrs={ 
                'Class': 'form-control', 
                'Placeholder': '',
                'min':'0',
            }),

            'Precio_de_venta': forms.NumberInput(attrs={ 
                'Class': 'form-control', 
                'Placeholder': '',
                'min':'0',
            }),

            'prod_imagen': forms.FileInput(attrs={
                'Class': 'form-control',
                'Placeholder': '',
            }), 

            'Estado' : forms.Select(attrs={
                'Class':'form-select', 
                'Placeholder':'Seleccione',
            }),

        } 

    def _init_(self, *args, **kwargs):

        super()._init_(*args, **kwargs) 
        
        self.fields['Catego_Id'].queryset = categoria.objects.only('Nombre')

        self.fields['Catego_Id'].label_from_instance = lambda objects: objects.Nombre