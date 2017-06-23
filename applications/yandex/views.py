# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic.base import View

try:
    from django.utils.importlib import import_module
except ImportError:
    import importlib

from django.utils.html import strip_tags
from django import db

from datetime import datetime
import time

from lxml import etree

try:
    from proj.settings import YML_CONFIG
except ImportError:
    YML_CONFIG = None

from applications.product.models import Product

# https://github.com/fmarchenko/django-shop-yml
__author__ = 'AlexStarov'


class GenerateShopYMLView(View):

    def get(self, request, *args, **kwargs):
        root = etree.Element('yml_catalog', date=datetime.today().strftime("%Y-%m-%d %H:%M"))
        shop = etree.SubElement(root, 'shop')

        etree.SubElement(shop, 'name').text = YML_CONFIG['name']
        etree.SubElement(shop, 'company').text = YML_CONFIG['company']
        etree.SubElement(shop, 'url').text = YML_CONFIG['url']

        currencies = etree.SubElement(shop, 'currencies')

        for currency in YML_CONFIG['currencies']:
            etree.SubElement(currencies, 'currency', rate=currency['rate'], id=currency['id'])

        db.reset_queries()
        start_time = time.time()
        self.set_categories(shop)
        print(" self.set_categories(shop) --- %s seconds ---" % (time.time() - start_time), len(db.connection.queries))
        # etree.SubElement(shop, 'local_delivery_cost').text = YML_CONFIG['local_delivery_cost']

        db.reset_queries()
        start_time = time.time()
        self.set_products(shop)
        print(" self.set_products(shop) --- %s seconds ---" % (time.time() - start_time), len(db.connection.queries))

        for conn in db.connection.queries:
            print('time: ', conn['time'], 'sql: ', conn['sql'], )

        # print etree.tostring(root)

        return HttpResponse(etree.tostring(root), content_type='text/xml')

    def set_categories(self, shop):
        class_path = YML_CONFIG['category_model']

        class_module, class_name = class_path.rsplit('.', 1)
        mod = importlib.import_module(class_module)
        clazz = getattr(mod, class_name)
        categories_tag = etree.SubElement(shop, 'categories')
        for category in clazz.objects.published().values('id', 'parent_id', 'title', ).order_by('id'):
            if not category['parent_id']:
                etree.SubElement(categories_tag,
                                 'category',
                                 id=str(category['id'])).text = category['title']  # .get_name()
            else:
                etree.SubElement(categories_tag,
                                 'category',
                                 id=str(category['id']),
                                 parentId=str(category['parent_id'])).text = category['title']  # .get_name()

    def set_products(self, shop):
        offers = etree.SubElement(shop, 'offers')
        i = 0
        for product in Product.objects.published().only('id', 'pk', 'is_availability', 'url', 'price', 'currency_id', 'name', 'description', 'in_action', ).prefetch_related('producttocategory_set').order_by('id'):

            if product.is_availability == 1:
                available = 'true'
            elif product.is_availability in [2, 3]:
                available = 'false'
            else:
                continue

            offer = etree.SubElement(offers, 'offer', id=str(product.id), available=available)

            etree.SubElement(offer, 'url').text = YML_CONFIG['url'] + product.get_absolute_url()
            etree.SubElement(offer, 'price').text = str(product.get_price())
            etree.SubElement(offer, 'currencyId').text = 'UAH'

            try:
                #print product._meta.get_all_field_names()
                etree.SubElement(offer, 'categoryId').text = \
                    str(product.producttocategory_set.all()[0].id, )
                    # str(product.category.all().only('id').values_list('id', flat=True)[0])
            except IndexError:
                pass
                # etree.SubElement(offer, 'picture').text = YML_CONFIG['url'] + product.head_image.url
            etree.SubElement(offer, 'delivery').text = 'true'
            etree.SubElement(offer, 'name').text = product.name
            etree.SubElement(offer, 'description').text = strip_tags(product.description)\
                .replace('&nbsp;', ' ',)\
                .replace('           ', ' ', )\
                .replace('          ', ' ', )\
                .replace('         ', ' ', )\
                .replace('        ', ' ', )\
                .replace('       ', ' ', )\
                .replace('      ', ' ', )\
                .replace('     ', ' ', )\
                .replace('    ', ' ', )\
                .replace('   ', ' ', )\
                .replace('  ', ' ', )
            #etree.SubElement(offer, 'name').text = product.get_name()
            etree.SubElement(offer, 'picture').text = 'https://keksik.com.ua{}'.format(product.main_photo.photo.url, )
            i += 1

            #self.bar.update(i)
