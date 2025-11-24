from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter
def currency_cop(value):
    """
    Formatea un número como moneda colombiana
    Ejemplo: 45000 -> $45.000
    """
    try:
        value = float(value)
        formatted = intcomma(int(value))
        return f"${formatted}"
    except (ValueError, TypeError):
        return value