from django import forms
from django.contrib.auth.models import Group, Permission
from .models import User_Empleados


class EmpleadoForm(forms.ModelForm):
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Contraseña",
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
        required=True
    )

    is_active = forms.ChoiceField(
        choices=[
            ('', 'Seleccione...'),
            ('True', 'Activo'),
            ('False', 'Inactivo')
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label="Estado del Usuario"
    )

    class Meta:
        model = User_Empleados
        fields = [
            'username', 'password', 'first_name', 'last_name', 'email',
            'Eps', 'Sexo', 'Cedula', 'Direccion', 'Celular', 'empleados_img',
            'is_active', 'groups', 'user_permissions'
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'Eps': forms.TextInput(attrs={'class': 'form-control'}),
            'Cedula': forms.NumberInput(attrs={'class': 'form-control'}),
            'Direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'Celular': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
            'empleados_img': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'user_permissions': forms.SelectMultiple(attrs={'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        usuario_actual = kwargs.pop('usuario_actual', None)
        super().__init__(*args, **kwargs)

        # Valores requeridos
        for campo in ['first_name', 'last_name', 'email', 'Cedula']:
            self.fields[campo].required = True

        # Filtrar grupos según permisos del usuario actual
        if usuario_actual and not usuario_actual.is_superuser:
            self.fields['groups'].queryset = Group.objects.exclude(name__iexact="admin")

        # Crear
        if not self.instance.pk:
            self.fields['password'].required = True
            self.fields['empleados_img'].required = True
            self.fields['is_active'].initial = 'True'
        else:
            # Editar
            self.fields['password'].help_text = "Deja en blanco para mantener la contraseña actual"

    def clean_is_active(self):
        val = self.cleaned_data['is_active']
        return val == 'True'

    def save(self, commit=True):
        user = super().save(commit=False)

        # Guardar contraseña correctamente
        pwd = self.cleaned_data.get('password')
        if pwd:
            user.set_password(pwd)

        if commit:
            user.save()
            self.save_m2m()

        return user
