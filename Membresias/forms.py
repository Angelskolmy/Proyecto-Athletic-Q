from django import forms
from .models import Membresia
from Tipo_membresia.models import TipoMembresia
from Empleados.models import User_Empleados

class MembresiaForm(forms.ModelForm):
    
    class Meta:
        model = Membresia
        fields = ['id_usuario', 'For_Id_tipo_membresia', 'Fecha_fin', 'Estado', 'membresia_img']
        
        widgets = {
            'id_usuario': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Seleccione un usuario'
            }),
            
            'For_Id_tipo_membresia': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Seleccione tipo de membresía'
            }),
            
            'Fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
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
            'id_usuario': 'Usuario',
            'For_Id_tipo_membresia': 'Tipo de Membresía',
            'Fecha_fin': 'Fecha de Finalización',
            'Estado': 'Estado',
            'membresia_img': 'Imagen de Membresía'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Mostrar solo usuarios activos
        self.fields['id_usuario'].queryset = User_Empleados.objects.filter(is_active=True).order_by('first_name')
        self.fields['id_usuario'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name} - {obj.Cedula}"
        
        # Mostrar solo tipos de membresía activos
        self.fields['For_Id_tipo_membresia'].queryset = TipoMembresia.objects.filter(Estado='Activo').order_by('Duracion_meses')
        self.fields['For_Id_tipo_membresia'].label_from_instance = lambda obj: f"{obj.Nombre} - ${obj.Precio} ({obj.get_Duracion_meses_display()})"
    
    def clean_Fecha_fin(self):
        fecha_fin = self.cleaned_data.get('Fecha_fin')
        if not fecha_fin:
            raise forms.ValidationError('La fecha de finalización es obligatoria')
        return fecha_fin