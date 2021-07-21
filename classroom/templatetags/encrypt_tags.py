from django import template
from e_learning.functions import encrypt as e, decrypt as d
register = template.Library()


@register.filter(name='encrypt')
def encrypt(value):
    string = e(value).replace('/', '?')
    return string
