from django import forms 
from .models import producto 
from .models import categoria

class ProductoForm(forms.ModelForm): 
    
    class Meta: 
        model=producto
        fields=['Catego_Id','Nombre','Descripcion','Stock','Precio_de_compra','Precio_de_venta','prod_imagen','Estado']

        widgets={

            'Nombre': forms.TextInput(attrs={
                'class':'form-control', 
                'placeholder':'Nombre',
            }), 
            
            'Catego_Id' : forms.Select(attrs={
                'class': 'form-select', 
                'placeholder':'Seleccione',
            }), 

            'Descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder' : '', 
                'rows' : 3, 
            }),

            'Stock':forms.NumberInput(attrs={
                'class': 'form-control numero', 
                'placeholder': '',
                'id': 'stock',
            }), 

            'Precio_de_compra': forms.NumberInput(attrs={ 
                'class': 'form-control numero', 
                'placeholder': '',
                'id':'precio_de_compra'
            }),

            'Precio_de_venta': forms.NumberInput(attrs={ 
                'class': 'form-control numero', 
                'placeholder': '',
                'id':'precio_de_venta'
            }),

            'prod_imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': '',
            }), 

            'Estado' : forms.Select(attrs={
                'class':'form-select', 
                'placeholder':'Seleccione',
            }),

        } 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        
        self.fields['Catego_Id'].queryset = categoria.objects.filter(Estado='Activo')
        self.fields['Catego_Id'].label_from_instance = lambda obj: obj.Nombre
        
        # Si es CREAR (no tiene pk), Estado = Activo y no editable
        if not self.instance.pk:
            self.fields['Estado'].initial = 'Activo'
            self.fields['Estado'].widget = forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'value': 'Activo'
            })
            