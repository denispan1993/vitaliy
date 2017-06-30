# -*- coding: utf-8 -*-
import time
from lxml import etree
from datetime import datetime
from django import db
from django.utils.html import strip_tags
from celery.utils.log import get_task_logger

from proj.celery import celery_app

from applications.product.models import Product
import os

try:
    from django.utils.importlib import import_module
except ImportError:
    import importlib

try:
    from proj.settings import YML_CONFIG
except ImportError:
    YML_CONFIG = None

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)


@celery_app.task(name='yml.tasks.generate_prom_ua_yml', )
def generate_prom_ua_yml(*args, **kwargs):

    start = datetime.now()
    logger.info(u'Start: generate_prom_ua_yml(*args, **kwargs): datetime.now() {0}'.format(start), )

    def set_categories(shop, ):

        class_module, class_name = YML_CONFIG['category_model'].rsplit('.', 1)
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

    def set_products(shop):
        offers = etree.SubElement(shop, 'offers')

        for product in Product.objects.published().only('id', 'pk', 'is_availability', 'url', 'price', 'currency_id', 'name', 'description', 'in_action', ).prefetch_related('producttocategory_set').order_by('id'):

            if product.is_availability == 1:
                available = 'true'
            elif product.is_availability in [2, 3]:
                available = 'false'
            else:
                continue

            offer = etree.SubElement(offers, 'offer', id=str(product.id), available=available)

            etree.SubElement(offer, 'url').text = YML_CONFIG['url'] + product.get_absolute_url()
            etree.SubElement(offer, 'price').text = str(float(product.get_price())*1.12)
            etree.SubElement(offer, 'currencyId').text = 'UAH'

            try:
                #print product._meta.get_all_field_names()
                etree.SubElement(offer, 'categoryId').text = \
                    str(product.producttocategory_set.all()[0].category_id, )
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
            try:
                etree.SubElement(offer, 'picture').text = 'https://keksik.com.ua{}'.format(product.main_photo.photo.url, )
            except AttributeError:
                pass

    """ ------------------------------------------------------------------------------------------ """
    """ Собственно сама генерация """
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
    set_categories(shop)
    logger.info(u'set_categories(shop) --- {0} seconds --- {1}'.format((time.time() - start_time), len(db.connection.queries), ), )

    db.reset_queries()
    start_time = time.time()
    set_products(shop)
    logger.info(u'set_products(shop) --- {0} seconds --- {1}'.format((time.time() - start_time), len(db.connection.queries), ), )

    files = [f for f in os.listdir('.')]
    for f in files:
        print(f)

    with open('/www/projs/prod.keksik_com_ua/storage/yml/prom.ua/shop.yml', 'w') as f:
        f.write(etree.tostring(root).decode('utf-8'))

    stop = datetime.now()
    logger.info(u'Stop: generate_prom_ua_yml(*args, **kwargs): datetime.now() {0} | {1}'.format(stop, (stop - start), ), )
