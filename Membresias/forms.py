from django import forms
from .models import Membresia
from Tipo_membresia.models import TipoMembresia
from Empleados.models import User_Empleados

class MembresiaForm(forms.ModelForm):
    
    class Meta:
        model = Membresia
        fields = ['id_usuario', 'For_Id_tipo_membresia', 'Estado', 'membresia_img']
        
        widgets = {
            'id_usuario': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Seleccione un usuario'
            }),
            
            'For_Id_tipo_membresia': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Seleccione tipo de membresía',
                'id': 'id_For_Id_tipo_membresia'
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
            'membresia_img': 'Imagen de Membresía (Opcional)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # SI ESTAMOS EDITANDO
        if self.instance and self.instance.pk:
            # Usuario solo lectura
            self.fields['id_usuario'].disabled = True
            self.fields['id_usuario'].widget.attrs.update({
                'class': 'form-select',
                'style': 'background-color: #e9ecef; cursor: not-allowed;'
            })
            
            # Tipo de membresía solo lectura
            self.fields['For_Id_tipo_membresia'].disabled = True
            self.fields['For_Id_tipo_membresia'].widget.attrs.update({
                'class': 'form-select',
                'style': 'background-color: #e9ecef; cursor: not-allowed;',
                'id': 'id_For_Id_tipo_membresia'
            })
        else:
            # SI ESTAMOS CREANDO, CONFIGURAR NORMALMENTE
            # Mostrar solo usuarios activos
            self.fields['id_usuario'].queryset = User_Empleados.objects.filter(
                is_active=True
            ).order_by('first_name')
            
            self.fields['id_usuario'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name} - Cédula: {obj.Cedula or 'N/A'}"
            
            # Mostrar solo tipos de membresía activos
            self.fields['For_Id_tipo_membresia'].queryset = TipoMembresia.objects.filter(
                Estado='Activo'
            ).order_by('Duracion_meses')
            
            self.fields['For_Id_tipo_membresia'].label_from_instance = lambda obj: (
                f"{obj.Nombre} - ${obj.Precio:,.0f} ({obj.get_Duracion_meses_display()})"
            )
        
        # Hacer la imagen opcional (siempre)
        self.fields['membresia_img'].required = False