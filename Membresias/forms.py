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
                'id': 'id_id_usuario',
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
            'id_usuario': 'Usuario',
            'For_Id_tipo_membresia': 'Tipo de Membresía',
            'Estado': 'Estado',
            'membresia_img': 'Imagen de la Membresía'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar usuarios del grupo "Usuarios" activos
        self.fields['id_usuario'].queryset = User_Empleados.objects.filter(
            groups__name='Usuarios',
            is_active=True
        ).order_by('first_name', 'last_name')
        
        self.fields['id_usuario'].empty_label = "Seleccione un usuario..."
        
        # Mostrar nombre completo y cédula del usuario
        self.fields['id_usuario'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name} - {obj.Cedula}"
        
        # Tipo de membresía - mostrar nombre
        self.fields['For_Id_tipo_membresia'].queryset = TipoMembresia.objects.filter(
            Estado='Activo'
        ).order_by('Duracion_meses', 'Precio')
        
        self.fields['For_Id_tipo_membresia'].empty_label = "Seleccione un tipo de membresía..."
        
        # Mostrar nombre del tipo de membresía
        self.fields['For_Id_tipo_membresia'].label_from_instance = lambda obj: f"{obj.Nombre} - {obj.Duracion_meses} mes(es) - ${obj.Precio:,.0f}"
        
        # Si es CREAR, Estado = Activo con input readonly
        if not self.instance.pk:
            self.fields['Estado'].initial = 'Activo'
            self.fields['Estado'].widget = forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'value': 'Activo'
            })
        else:
            # Si es EDITAR, deshabilitar usuario y tipo
            self.fields['id_usuario'].disabled = True
            self.fields['For_Id_tipo_membresia'].disabled = True
            self.fields['id_usuario'].widget.attrs['style'] = 'background-color: #e9ecef;'
            self.fields['For_Id_tipo_membresia'].widget.attrs['style'] = 'background-color: #e9ecef;'