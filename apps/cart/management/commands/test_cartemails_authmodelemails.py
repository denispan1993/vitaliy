# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.core.management.base import BaseCommand

from pytils.translit import slugify


class Command(BaseCommand, ):
    def handle(self, *args, **options):
        from apps.cart.models import Order
        orders = Order.objects.all()
        from apps.authModel.models import Email
        for order in orders:
            try:
                email = Email.objects.get(email=order.email, )
            except Email.DoesNotExist:
                print order.email
