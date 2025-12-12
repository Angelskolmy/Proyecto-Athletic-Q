from django import forms
from .models import Venta
from Empleados.models import User_Empleados

PAYMENT_CHOICES = [ 
    ('Efectivo', 'Efectivo'),
    ('Credito', 'Crédito'),
    ('Debito', 'Débito'),
    ('PSE', 'PSE'),
    ('Nequi', 'Nequi'),
]

class VentaForm(forms.ModelForm):
    
    # Campo para seleccionar cliente (usuario registrado o fantasma)
    cliente = forms.ModelChoiceField(
        queryset=User_Empleados.objects.filter(
            groups__name='Usuarios',
            is_active=True
        ).order_by('first_name'),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'cliente-select',
            'required': True
        }),
        label='Cliente (Seleccionar)',
        required=False  # Hacerlo opcional porque puede ser fantasma
    )
    
    metodo_pago = forms.ChoiceField(
        choices=[('', 'Seleccione el metodo de pago...')] + PAYMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'metodo_pago'}),
        required=True,
        label='Método de Pago'
    )

    class Meta:
        model = Venta
        fields = ['id_usuario', 'Numero_Transaccion', 'Cedula_Vents']
        widgets = {
            'id_usuario': forms.HiddenInput(),
            'Numero_Transaccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 123RF4',
                'id': 'Numero_Transaccion'
            }),
            'Cedula_Vents': forms.NumberInput(attrs={
                'class': 'form-control numero',
                'placeholder': 'Cédula del cliente...',
                'id': 'Cedula_Vents'
            }),
        }
        labels = {
            'Numero_Transaccion': 'Número de Transacción',
            'Cedula_Vents': 'Cédula (comprador)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Personalizar la etiqueta del cliente
        self.fields['cliente'].label_from_instance = lambda obj: (
            f"{obj.get_full_name()} - Cédula: {obj.Cedula}" 
            if obj.Cedula != 0 
            else "Cliente Sin Registro (Fantasma)"
        )
    
    def clean_Cedula_Vents(self):
        """La cédula se llena automáticamente desde el cliente seleccionado"""
        cedula = self.cleaned_data.get('Cedula_Vents')
        # No validar aquí, se llena automáticamente en JavaScript
        return cedula