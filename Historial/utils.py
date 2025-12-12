from django.utils import timezone

from .models import Historial_usuario


def registrar_movimiento(user, tipo, modulo, nombre_objeto, id_objeto):
    """
    Crea un registro en el historial de movimientos.
    `nombre_objeto` se trunca a 50 caracteres para evitar errores en DB.
    """
    if not nombre_objeto:
        nombre_objeto = ''

    Historial_usuario.objects.create(
        id_usuario=user,
        TIpo_Movimiento=tipo,
        Modulo=modulo,
        Nombre_Objeto=nombre_objeto[:50],
        Id_Objeto=id_objeto,
        Fecha_y_hora=timezone.now().date(),
    )
