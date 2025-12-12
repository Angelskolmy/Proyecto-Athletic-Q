from django import template

register = template.Library()


def _get_variant(value: str) -> str:
    """
    Clasifica el estado recibido en success / warning / danger / neutral
    según palabras clave comunes en el flujo de asistencias.
    """
    if not value:
        return "neutral"

    estado = value.strip().lower()

    success_keywords = (
        "complet", "salid", "registrad", "presen", "activo", "cumpl", "cerrad"
    )
    warning_keywords = (
        "pend", "en proceso", "entrada", "ingres", "espera", "abiert", "verificando"
    )
    danger_keywords = (
        "ausent", "cancel", "incomplet", "fall", "tarde", "incumpl", "rechaz", "error"
    )

    if any(word in estado for word in success_keywords):
        return "success"

    if any(word in estado for word in warning_keywords):
        return "warning"

    if any(word in estado for word in danger_keywords):
        return "danger"

    return "neutral"


@register.filter
def estado_badge_class(value: str) -> str:
    """Devuelve la clase CSS para la insignia del estado."""
    return f"estado-badge--{_get_variant(value)}"


@register.filter
def estado_row_class(value: str) -> str:
    """Devuelve la clase CSS para resaltar la fila completa."""
    return f"estado-row--{_get_variant(value)}"
