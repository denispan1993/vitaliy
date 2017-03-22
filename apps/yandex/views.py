# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic.base import View
from django.utils.importlib import import_module

from datetime import datetime

from lxml import etree

__author__ = 'AlexStarov'

YML_CONFIG = {'name': u'Название магазина',
              'company': u'Название компании',
              'url': 'http://example.com',
              'currencies': ({'id': "RUR", 'rate': "1"}, ),
              'category_model': 'apps.product.models.Category',
              'local_delivery_cost': u'Бесплатно в Москве', }


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

        return HttpResponse('Hello, World!')

    def set_categories(self, shop):
        class_path = YML_CONFIG['category_model']

        class_module, class_name = class_path.rsplit('.', 1)
        mod = import_module(class_module)
        clazz = getattr(mod, class_name)
        categories_tag = etree.SubElement(shop, 'categories')
        for category in clazz.objects.all():
            etree.SubElement(categories_tag, 'category', id=str(category.id)).text = category.get_name()
