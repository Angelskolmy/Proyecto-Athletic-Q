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

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['id_usuario'].queryset = User_Empleados.objects.all()

    def clean_Cedula_Vents(self):
        cedula = self.cleaned_data.get('Cedula_Vents')
        
        if cedula:
            # Verificar si la cédula existe en empleados
            existe_cedula = User_Empleados.objects.filter(Cedula=cedula).exists()
            if not existe_cedula:
                # Si no existe, permitir guardarla igual (se usará usuario fantasma)
                pass
        
        return cedula