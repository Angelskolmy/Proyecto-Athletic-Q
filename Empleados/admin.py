from django.contrib import admin
from .models import User_Empleados

class UserEmpleadosAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff')

    def save_model(self, request, obj, form, change):
        raw_password = form.cleaned_data.get("password")

        if raw_password and not raw_password.startswith("pbkdf2_"):
            obj.set_password(raw_password)

        obj.save()

admin.site.register(User_Empleados, UserEmpleadosAdmin)