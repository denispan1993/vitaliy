# -*- coding: utf-8 -*-
from time import sleep
from django.core.management.base import BaseCommand
import celery

from applications.cart.models import Order
from applications.cart.tasks import recompile_order

__author__ = 'AlexStarov'
""" Парсим заказы - переводим Email-ы в базу Email-ов а телефоны в базу телефонов. """


class Command(BaseCommand, ):

    def handle(self, *args, **options):

        orders = Order.objects.all().order_by('pk')
        for i, order in enumerate(start=1, iterable=orders, ):

            print('i:', i, 'pk:', order.pk, 'order.user:', order.user, 'order:', order, )

            if order.user:
                sleep(0.1, )
                continue

            else:
                recompile_order.apply_async(
                    queue='celery',
                    kwargs={'order_pk': order.pk, },
                    task_id='celery-task-id-recompile_order-{0}'.format(celery.utils.uuid(), ),
                )

            sleep(1, )
