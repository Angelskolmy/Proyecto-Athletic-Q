from django import forms
from .models import categoria

class CrearCategoriaForm(forms.ModelForm):
    Estado = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'value': 'Activo',
            'readonly': True
        }),
        initial='Activo'
    )

    class Meta:
        model = categoria
        fields = ['Nombre', 'Estado']
        widgets = {
            'Nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la categoría',
                'required': True
            })
        }
        labels = {
            'Nombre': 'Nombre de la Categoría',
            'Estado': 'Estado'
        }

class EditarCategoriaForm(forms.ModelForm):
    class Meta:
        model = categoria
        fields = ['Nombre', 'Estado']
        widgets = {
            'Nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la categoría',
                'required': True
            }),
            'Estado': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])
        }
        labels = {
            'Nombre': 'Nombre de la Categoría',
            'Estado': 'Estado'
        }