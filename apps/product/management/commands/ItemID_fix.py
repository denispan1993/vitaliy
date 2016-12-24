# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from apps.product.models import ItemID

__author__ = 'AlexStarov'
""" Фиксим Артикулы. """


class Command(BaseCommand, ):

    def handle(self, *args, **options):

        for item in ItemID.objects.all():

            if item.parent:
                item.ItemID = item.ItemID.replace(' ', '', )
            else:
                print(item.pk, ': ', item.ItemID, )
                continue

            item.save()
