from django.contrib import admin
from .models import User_Empleados

class UserEmpleadosAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff')

    def save_model(self, request, obj, form, change):
        raw_password = form.cleaned_data.get("password")

        # Solo cambiar contraseña si NO está vacío
        if raw_password and raw_password.strip():  # Verificar que no esté vacío
            obj.set_password(raw_password)
        elif change:  # Si es edición y la contraseña está vacía, mantener la actual
            # No hacer nada - mantiene la contraseña anterior
            pass

        obj.save()

admin.site.register(User_Empleados, UserEmpleadosAdmin)