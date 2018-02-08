from django import template

register = template.Library()


@register.filter
def get_at_index(list, index):
    try:
        element = list[index]
    except IndexError:
        element = '100%'
    return element
