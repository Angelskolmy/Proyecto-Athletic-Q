from django import forms
from django.contrib.auth.forms import SetPasswordForm


class CambiaContraseñaForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

        self.fields["new_password1"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control boton",
                "placeholder": "Nueva contrasena",
            }
        )

        self.fields["new_password2"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control boton",
                "placeholder": "Confirmar contrasena",
            }
        )

        self.fields["new_password1"].label = "Nueva contrasena"
        self.fields["new_password2"].label = "Confirmar contrasena"
