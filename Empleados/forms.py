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
                'Eps', 'Sexo', 'Cedula', 'empleados_img', 'is_active', 'groups', 'user_permissions']  # Agregar Huella_id
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de usuario'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre',
                'pattern': '[a-zA-Z0-9]+',
                'title': 'Solo se permiten letras y números'
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
                'placeholder': 'Ingrese la cédula',
                'pattern': '{10,11}', 
                'title': 'La cédula debe tener entre 10 y 11 números'
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
            'is_active': 'Estado del Usuario'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['Eps'].required = False
        self.fields['Sexo'].required = True 
        self.fields['Cedula'].required = True
        self.fields['empleados_img'].required = True
        self.fields['is_active'].required = True
        self.fields['groups'].required = True
        
        # Si estamos editando, hacer password opcional
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
            self.fields['password'].help_text = 'Deja en blanco para mantener la contraseña actual'
            
            # Pre-seleccionar el grupo actual
            if self.instance.pk:
                grupos = self.instance.groups.all()
                if grupos.exists():
                    self.fields['groups'].initial = grupos.first().id
                
            # Pre-seleccionar los permisos actuales
            self.fields['user_permissions'].initial = self.instance.user_permissions.all()
        
        # Organizar permisos por aplicación para mejor visualización
        self.fields['user_permissions'].queryset = Permission.objects.all().order_by('content_type__app_label', 'name')