from django import forms
from .models import Membresia
from Empleados.models import User_Empleados

class MembresiaForm(forms.ModelForm):
    
    class Meta:
        model = Membresia
        fields = ['id_usuario', 'Duracion_meses', 'Precio', 'Estado']
        
        widgets = {
            'id_usuario': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Duracion_meses': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duración en meses',
                'min': 1,
                'max': 24,
                'required': True
            }),
            'Precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio de la membresía',
                'min': 0,
                'step': 0.01,
                'required': True
            }),
            'Estado': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            })
        }
        
        labels = {
            'id_usuario': 'Cliente',
            'Duracion_meses': 'Duración (meses)',
            'Precio': 'Precio ($)',
            'Estado': 'Estado'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personalizar el queryset para mostrar nombre completo
        usuarios = User_Empleados.objects.filter(is_active=True).order_by('first_name', 'last_name')
        choices = [('', 'Seleccione un cliente...')]
        for usuario in usuarios:
            nombre_completo = f"{usuario.first_name} {usuario.last_name}"
            if usuario.Cedula:
                nombre_completo += f" - {usuario.Cedula}"
            choices.append((usuario.id, nombre_completo))
        
        self.fields['id_usuario'].choices = choices
        
        # Personalizar las opciones de Estado
        self.fields['Estado'].choices = [
            ('', 'Seleccione el estado...'),
            ('Activo', 'Activo'),
            ('Inactivo', 'Inactivo')
        ]

    def clean_id_usuario(self):
        id_usuario = self.cleaned_data.get('id_usuario')
        if not id_usuario:
            raise forms.ValidationError('Debe seleccionar un cliente.')
        return id_usuario

    def clean_Duracion_meses(self):
        duracion = self.cleaned_data.get('Duracion_meses')
        if not duracion or duracion < 1 or duracion > 24:
            raise forms.ValidationError('La duración debe estar entre 1 y 24 meses.')
        return duracion

    def clean_Precio(self):
        precio = self.cleaned_data.get('Precio')
        if not precio or precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor que 0.')
        return precio

    def clean_Estado(self):
        estado = self.cleaned_data.get('Estado')
        if not estado:
            raise forms.ValidationError('Debe seleccionar un estado.')
        return estado