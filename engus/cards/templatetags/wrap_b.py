import re
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.template.defaultfilters import escape

register = template.Library()

@register.filter(name='wrap_b')
@stringfilter
def wrap_b(value, substring):
    if len(substring) > 0 and re.search(substring, value):
        value = escape(value)
        substring = escape(substring)
        value = mark_safe(value.replace(substring, '<b>%s</b>' % substring))
    return value