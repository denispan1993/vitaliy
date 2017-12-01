# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.core.management.base import BaseCommand

from pytils.translit import slugify


class Command(BaseCommand, ):
    def handle(self, *args, **options):
        from applications.cart.models import Order
        orders = Order.objects.all()
        from applications.authModel.models import Email
        for order in orders:
            try:
                email = Email.objects.get(email=order.email, )
            except Email.DoesNotExist:
                print('SessionID: ', order.sessionid, 'E-Mail: ', order.email, )
            except Email.MultipleObjectsReturned:
                emails = Email.objects.filter(email=order.email, )
                print('MultiObject: ', emails[0].email, )
