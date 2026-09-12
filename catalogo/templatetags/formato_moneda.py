from django import template

register = template.Library()


@register.filter
def moneda(valor):
    if valor is None:
        return "$0"

    return "${:,.0f}".format(valor).replace(",", ".")