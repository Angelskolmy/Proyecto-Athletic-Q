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
                'placeholder': '0.00',
                'step': '0.01',
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
            'Nombre': 'Nombre del Tipo de Membresía',
            'Duracion_meses': 'Duración',
            'Precio': 'Precio',
            'Estado': 'Estado',
            'tipo_membresia_img': 'Imagen'
        }
    
    def clean_Precio(self):
        precio = self.cleaned_data.get('Precio')
        if precio and precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo')
        return precio