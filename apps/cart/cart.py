# -*- coding: utf-8 -*-
# /apps/cart/cart.py
from django.shortcuts import render, redirect
from .utils import get_cart_or_create

__author__ = 'AlexStarov'


def show_cart(request,
              template_name=u'show_cart.jinja2', ):

    return render(request=request, template_name=template_name, )


def recalc_cart(request, ):
    from .models import Product
    if request.method == 'POST' and request.POST.get('POST_NAME', None, ) == 'recalc_cart':

        """ Взять корзину """
        product_cart, created = get_cart_or_create(request, )

        try:
            """ Выборка всех продуктов из корзины """
            for product_in_cart in product_cart.cart.all():
                """ Нужно проверить, есть ли вообще такой продукт в корзине? """
                product_in_request_pk = request.POST.get(u'product_in_request_%d' % product_in_cart.pk, None, )

                try:
                    product_in_request_pk = int(product_in_request_pk, )
                except (ValueError, TypeError, ):
                    continue

                if product_in_request_pk == product_in_cart.pk:
                    product_del = request.POST.get(u'delete_%d' % product_in_cart.pk, None, )

                    if product_del:
                        product_in_cart.product_delete
                        continue

                    product_quantity = request.POST.get(u'quantity_%d' % product_in_cart.pk, None, )
                    if product_quantity != product_in_cart.quantity:
                        product_in_cart.update_quantity(product_quantity, )
                        continue
                else:
                    continue

        except Product.DoesNotExist:
            """ Странно!!! В корзине нету продуктов!!! """
            pass

    return redirect(to='cart:show_cart', )
