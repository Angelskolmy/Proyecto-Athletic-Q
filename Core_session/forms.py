from django import forms
from django.contrib.auth.forms import SetPasswordForm

class CambiaContraseñaForm(SetPasswordForm):

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)

        # Campo 1
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control boton',
            'placeholder': 'Contraseña'
        })

        # Campo 2
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control boton',
            'placeholder': 'Confirmar contraseña'
        })

        # Cambiar textos de labels
        self.fields['new_password1'].label = "Nueva contraseña"
        self.fields['new_password2'].label = "Confirmar contraseña"