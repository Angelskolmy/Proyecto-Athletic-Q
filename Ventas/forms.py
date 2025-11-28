from django import forms
from .models import Venta
from Detalle_venta.models import Detalle_Venta
from Empleados.models import User_Empleados

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['id_usuario']
        
        widgets = {
            'id_usuario': forms.Select(attrs={
                'class': 'form-select',
            })
        }
        
        labels = {
            'id_usuario': 'Vendedor'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo empleados activos
        self.fields['id_usuario'].queryset = User_Empleados.objects.filter(
            is_active=True, 
            is_staff=True
        ).order_by('first_name')


# Formulario para editar ventas (admin)
class EditarVentaForm(forms.Form):
    
    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describa el motivo de la edición de esta venta (obligatorio)...'
        }),
        label='Motivo de la Edición',
        required=True,
        help_text='Este campo es obligatorio para mantener un registro de auditoría'
    )
    
    metodo_pago = forms.ChoiceField(
        choices=[
            ('Efectivo', 'Efectivo'),
            ('Credito', 'Crédito'),
            ('Debito', 'Débito'),
            ('PSE', 'PSE'),
            ('Nequi', 'Nequi'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Método de Pago'
    )