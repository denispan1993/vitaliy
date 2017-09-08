# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from applications.product.models import Product


class Command(BaseCommand, ):

    def handle(self, *args, **options):

        for product in Product.objects.\
                published().\
                only('id', 'pk', 'is_availability', 'url', 'price',
                     'currency_id', 'name', 'description', 'in_action', ).\
                prefetch_related('producttocategory_set').\
                order_by('id'):

            category = product.producttocategory_set.filter(is_main=True)
            if category:
                if len(category) == 1:
                    # print(category[0].category)
                    pass
                else:
                    for cat in category:
                        print(product, cat.category)
            else:
                print('None: ', product)
