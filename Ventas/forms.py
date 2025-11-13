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