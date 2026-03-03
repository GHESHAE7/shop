from django import template



register = template.Library()


@register.filter
def res_discount(value, price):
    result = price - ((price / 100) * value)
    return int(result)