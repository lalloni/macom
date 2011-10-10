'''
Created on 08/10/2011

@author: plalloni
'''

from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.filter
@stringfilter
def ifnone(value, alternative):
    if value == None:
        return alternative
    else:
        return value
