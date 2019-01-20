from django import template
from django.shortcuts import get_object_or_404
from watsons.models import Transaction, Product, Customer, Pocket_other, Servive

register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    return value*arg

@register.filter(name='getProduct')
def getProduct(value):
    p = get_object_or_404(Product, id=value)
    return p

@register.filter(name='getPrice')
def getPrice(value):
    return value.price
