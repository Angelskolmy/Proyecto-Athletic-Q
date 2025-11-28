from django import forms
from .models import Membresia
from Empleados.models import User_Empleados
from Tipo_membresia.models import TipoMembresia

class MembresiaForm(forms.ModelForm):
    
    class Meta:
        model = Membresia
        fields = ['id_usuario', 'For_Id_tipo_membresia', 'Estado', 'membresia_img']
        
        widgets = {
            'id_usuario': forms.Select(attrs={
                'class': 'form-select',
            }),
            
            'For_Id_tipo_membresia': forms.Select(attrs={
                'class': 'form-select',
            }),
            
            'Estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            'membresia_img': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        
        labels = {
            'id_usuario': 'Cliente',
            'For_Id_tipo_membresia': 'Tipo de Membresía',
            'Estado': 'Estado',
            'membresia_img': 'Imagen de la Membresía'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # PLACEHOLDER PARA CLIENTE
        self.fields['id_usuario'].empty_label = "Seleccione un cliente"
        self.fields['id_usuario'].queryset = User_Empleados.objects.filter(
            is_active=True,
            groups__name='Clientes'
        ).order_by('first_name', 'last_name')
        
        # PLACEHOLDER PARA TIPO DE MEMBRESÍA
        self.fields['For_Id_tipo_membresia'].empty_label = "Seleccione un tipo de membresia"
        self.fields['For_Id_tipo_membresia'].queryset = TipoMembresia.objects.filter(
            Estado='Activo'
        ).order_by('Duracion_meses', 'Precio')
        
        # Deshabilitar campos en modo edición
        if self.instance and self.instance.pk:
            self.fields['id_usuario'].disabled = True
            self.fields['For_Id_tipo_membresia'].disabled = True
            self.fields['id_usuario'].widget.attrs['style'] = 'background-color: #e9ecef;'
            self.fields['For_Id_tipo_membresia'].widget.attrs['style'] = 'background-color: #e9ecef;'