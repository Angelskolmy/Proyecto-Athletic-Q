from django import forms
from django.contrib.auth.models import Group, Permission
from .models import User_Empleados

class EmpleadoForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la contraseña'
        }),
        required=False
    )
    
    # Campo para seleccionar grupo/rol
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Seleccione un rol...",
        required=False,
        label="Rol del Usuario"
    )
    
    # Campo para huella dactilar
    Huella_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'ID de huella dactilar',
            'readonly': True  # Solo lectura porque se asigna automáticamente
        }),
        required=False,
        label="ID de Huella Dactilar"
    )
    
    Sexo = forms.ChoiceField(
        choices=[('', 'Seleccione el género...')] + User_Empleados.Sexo_choice,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    is_active = forms.ChoiceField(
        choices=[('', 'Seleccione el estado...'), (True, 'Activo'), (False, 'Inactivo')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    class Meta:
        model = User_Empleados
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 
                 'Eps', 'Sexo', 'Cedula', 'empleados_img', 'Huella_id', 'is_active', 'groups', 'user_permissions']  # Agregar Huella_id
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de usuario'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ingrese el apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el correo'
            }),
            'Eps': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la EPS'
            }),
            'Cedula': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la cédula'
            }),
            'empleados_img': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

        labels = {
            'username': 'Nombre de Usuario',
            'password': 'Contraseña',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'Eps': 'EPS',
            'Sexo': 'Género',
            'Cedula': 'Número de Cédula',
            'empleados_img': 'Foto de Perfil',
            'Huella_id': 'ID de Huella Dactilar',
            'is_active': 'Estado del Usuario'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si estamos editando, hacer password opcional
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
            self.fields['password'].help_text = 'Deja en blanco para mantener la contraseña actual'
            
            # Pre-seleccionar el grupo actual
            if self.instance.groups.exists():
                self.fields['groups'].initial = self.instance.groups.first()
                
            # Pre-seleccionar los permisos actuales
            self.fields['user_permissions'].initial = self.instance.user_permissions.all()
        
        # Organizar permisos por aplicación para mejor visualización
        self.fields['user_permissions'].queryset = Permission.objects.all().order_by('content_type__app_label', 'name')