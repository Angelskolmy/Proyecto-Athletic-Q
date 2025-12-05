from django import forms
from .models import TipoMembresia

class TipoMembresiaForm(forms.ModelForm):
    
    class Meta:
        model = TipoMembresia
        fields = ['Nombre', 'Duracion_meses', 'Precio', 'Estado', 'tipo_membresia_img']
        
        widgets = {
            'Nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Premium Anual'
            }),
            
            'Duracion_meses': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            'Precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0'
            }),
            
            'Estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            'tipo_membresia_img': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        
        labels = {
            'Nombre': 'Nombre',
            'Duracion_meses': 'Duración',
            'Precio': 'Precio',
            'Estado': 'Estado',
            'tipo_membresia_img': 'Imagen'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si es CREAR, Estado = Activo con input readonly
        if not self.instance.pk:
            self.fields['Estado'].initial = 'Activo'
            self.fields['Estado'].widget = forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'value': 'Activo'
            })