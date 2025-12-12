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
    
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Seleccione un rol...",
        required=False,
        label="Rol del Usuario"
    )
    
    Sexo = forms.ChoiceField(
        choices=[('', 'Seleccione el género...')] + User_Empleados.SEXO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    TipoDocumento = forms.ChoiceField(
        choices=[('', 'Seleccione el tipo de documento...')] + User_Empleados.TIPO_DOC_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label="Tipo de documento"
    )
    
    is_active = forms.ChoiceField(
        choices=[('', 'Seleccione el estado...'), (True, 'Activo'), (False, 'Inactivo')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    class Meta:
        model = User_Empleados
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 
                'Eps', 'Sexo', 'TipoDocumento', 'Cedula', 'Direccion', 'Celular', 'empleados_img', 
                'is_active', 'groups', 'user_permissions']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de usuario'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre',
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
                'class': 'form-control numero',
                'placeholder': 'Ingrese la cédula',
            }),
            'Direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la dirección'
            }),
            'Celular': forms.TextInput(attrs={
                'class': 'form-control numero-celular',
                'placeholder': 'Ingrese el número de celular',
                'maxlength': '10'
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
            'Direccion': 'Dirección',
            'Celular': 'Número de Celular',
            'empleados_img': 'Foto de Perfil',
            'is_active': 'Estado del Usuario',
            'Cedula': 'Número de documento',
        }

    def __init__(self, *args, **kwargs):
        usuario_actual = kwargs.pop('usuario_actual', None)
        super().__init__(*args, **kwargs)
        
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['Eps'].required = False
        self.fields['Sexo'].required = True
        self.fields['TipoDocumento'].required = True 
        self.fields['Cedula'].required = True
        self.fields['Direccion'].required = False
        self.fields['Celular'].required = False
        self.fields['is_active'].required = True
        self.fields['groups'].required = True
        
        # Filtrar grupos según el usuario actual
        if usuario_actual:
            if usuario_actual.groups.filter(name__iexact="admin").exists() or usuario_actual.is_superuser:
                self.fields['groups'].queryset = Group.objects.all().order_by('name')
            else:
                self.fields['groups'].queryset = Group.objects.exclude(name__iexact="admin").order_by('name')
        
        # Si es CREAR
        if not self.instance.pk:
            self.fields['is_active'].initial = True
            self.fields['password'].required = True
            self.fields['empleados_img'].required = True
            self.fields['password'].help_text = 'La contraseña es obligatoria'
        else:
            # Si es EDITAR
            self.fields['password'].required = False
            self.fields['password'].help_text = 'Deja en blanco para mantener la contraseña actual'
            self.fields['empleados_img'].required = False
        
        # Organizar permisos por aplicación
        self.fields['user_permissions'].queryset = Permission.objects.all().order_by('content_type__app_label', 'name')

    def clean_password(self):
        """Validar la contraseña"""
        password = self.cleaned_data.get('password', '').strip()
        
        # Si es creación y no hay contraseña, error
        if not self.instance.pk and not password:
            raise forms.ValidationError("La contraseña es requerida al crear un usuario.")
        
        # Si es edición y el campo viene vacío → mantenemos la contraseña actual
        if self.instance.pk and not password:
            return self.instance.password
        
        # Si escribió algo, lo devolvemos (luego la vista decidirá si hacer set_password)
        return password
    
    def clean_Cedula(self):
        ced = self.cleaned_data.get('Cedula')

        if ced is None:
            raise forms.ValidationError("El número de documento es obligatorio.")

        ced_str = str(ced)
        if len(ced_str) < 5 or len(ced_str) > 12:
            raise forms.ValidationError("El documento debe tener entre 5 y 12 dígitos.")

        return ced


