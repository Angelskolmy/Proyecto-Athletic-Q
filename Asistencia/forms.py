from django import forms
from .models import Asistencia

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ["id_usuario", "rol", "fecha_entrada", "fecha_salida", "estado"]
        widgets = {
            "id_usuario": forms.Select(attrs={"class": "form-control"}),
            "rol": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_entrada": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "fecha_salida": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "estado": forms.TextInput(attrs={"class": "form-control"}),
        }