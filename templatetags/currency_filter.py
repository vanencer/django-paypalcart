from django import template
import locale

locale.setlocale(locale.LC_ALL, '')
register = template.Library() 
 
@register.filter()
def currency(value):
    if not isinstance(value, int):
        return ''
        
    value /= 100
    return locale.currency(value, grouping=True)