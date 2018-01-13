# -*- coding: utf-8 -*-
import time
import cProfile
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


def profile(func):
    """Decorator for run function profile"""

    def wrapper(*args, **kwargs):
        profile_filename = func.__name__ + '.prof'
        profiler = cProfile.Profile()
        result = profiler.runcall(func, *args, **kwargs)
        profiler.dump_stats(profile_filename)
        return result

    return wrapper


def decorate(func):
    # start = time.time()
    # print('Декорируем %s(*args, **kwargs): | Start: %s' % (func.__name__, start, ), )
    # logger.info('Декорируем %s... | Start: %s' % (func.__name__, start, ), )

    def wrapped(*args, **kwargs):
        start = time.time()
        print('Декорируем %s(*args, **kwargs): | Start: %s' % (func.__name__, start,), )
        logger.info('Декорируем %s... | Start: %s' % (func.__name__, start,), )

        print('Вызываем обёрнутую функцию с аргументами: *args и **kwargs ', )
        logger.info('Вызываем обёрнутую функцию с аргументами: *args и **kwargs ', )
        result = func(*args, **kwargs)

        stop = time.time()
        print('выполнено! | Stop: %s | Running time: %s' % (stop, stop - start,), )
        logger.info('выполнено! | Stop: %s | Running time: %s' % (stop, stop - start,), )

        return result

    # stop = time.time()
    # print('выполнено! | Stop: %s | Running time: %s' % (stop, stop - start, ), )
    # logger.info('выполнено! | Stop: %s | Running time: %s' % (stop, stop - start, ), )

    return wrapped


@celery_app.task(name='yml.tasks.generate_prom_ua_yml', )
# @profile
@decorate
def generate_prom_ua_yml(*args, **kwargs):

    start = time.time()
    start_datetime = datetime.now()
    logger.info('Start: generate_prom_ua_yml(*args, **kwargs): datetime.now() {0}'.format(start_datetime), )

    def set_categories(shop, ):

        class_module, class_name = YML_CONFIG['category_model'].rsplit('.', 1)
        mod = importlib.import_module(class_module)
        clazz = getattr(mod, class_name)
        categories_tag = etree.SubElement(shop, 'categories')
        for category in clazz.objects.published().values('id', 'parent_id', 'title', ).order_by('title'):
            if not category['parent_id']:
                etree.SubElement(categories_tag,
                                 'category',
                                 portal_id='15230431',  #Дом и сад	Посуда	Кухонные принадлежности	Кондитерские инструменты и аксессуары	https://prom.ua/Konditerskie-instrumenty-i-aksessuary
                                 id=str(category['id'])).text = category['title']  # .get_name()
            else:
                etree.SubElement(categories_tag,
                                 'category',
                                 portal_id='15230431',  #Дом и сад	Посуда	Кухонные принадлежности	Кондитерские инструменты и аксессуары	https://prom.ua/Konditerskie-instrumenty-i-aksessuary
                                 id=str(category['id']),
                                 parentId=str(category['parent_id'])).text = category['title']  # .get_name()

    def set_products(shop, ):
        offers = etree.SubElement(shop, 'offers')

        for product in Product.objects \
                .published() \
                .only('id', 'pk', 'is_availability', 'url', 'price',
                      'currency_id', 'name', 'description', 'in_action', ) \
                .prefetch_related('producttocategory_set') \
                .order_by('id'):

            """ Проверяем, стоит ли (выделена ли) у продукта "Основная" Категория """
            category = product.producttocategory_set.filter(is_main=True)
            if len(category) > 1:
                logger.info('generate_prom_ua_yml(*args, **kwargs): Many MAIN categories in product: {0}'.format(product), )
            elif len(category) < 1:
                """ Если нет, то берем первую попавшуюся """
                category = product.producttocategory_set.all()

            category = category.first()

            if category and not category.category.is_active:
                continue

            available = ''
            if product.is_availability == 1:
                available = 'true'
            elif product.is_availability in [2, 3, 4, ]:
                available = 'false'

            """
            Параметр selling_type ― это тип товара на Prom.ua. Тип_товара определяет размещение товара в каталоге по признаку оптовой продажи. Тип «Услуга» предназначен для размещения услуг, предоставляемых частным лицам или компаниям. Внимание! Данный параметр используется только на Prom.ua. Файл с данным параметром может вызывать ошибку при импорте в другие системы. Возможные значения: r, w, u, s.

                r — «Товар продается только в розницу» для потребительских и промышленных товаров с розничными ценами.
                w — «Товар продается только оптом» для потребительских и промышленных товаров, которые продаются только оптом.
                u — «Товар продается оптом и в розницу» для товаров, которые продаются и оптом и в розницу.
                s — услуга.
            """
            """
            Параметр "available" используется для указания статуса наличия товара. Значение «склад» или «true» соответствует статусу товара «В наличии», значение «false» — статусу «Под заказ». Если в данном поле пусто — товар будет импортирован в статусе «Нет в наличии».
            """
            offer = etree.SubElement(offers, 'offer', id=str(product.id), available=available, selling_type="r", )

            """
            <available>Наличие</available>
            Указание наличия для товара. Значение «склад» или «true» соответствует статусу товара «В наличии», значение «false» — статусу «Под заказ». Если в данном поле пусто — товар будет импортирован в статусе «Нет в наличии».
            """
            etree.SubElement(offer, 'available').text = available

            """
            <quantity_in_stock>Количество товара на складе</quantity_in_stock>
            Используется для указания остатка товаров на складе.
            """
            etree.SubElement(offer, 'quantity_in_stock').text = str(product.quantity_in_stock)

            if category:
                etree.SubElement(offer, 'categoryId').text = str(category.category_id, )
            else:
                logger.info('product.pk without category: {0}'.format(product.pk, ), )

            etree.SubElement(offer, 'url').text = YML_CONFIG['url'] + product.get_absolute_url()

            price = product.get_price()
            etree.SubElement(offer, 'price').text = price if price > 0 else 0.001

            etree.SubElement(offer, 'currencyId').text = 'UAH'

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

            try:
                etree.SubElement(offer, 'picture').text =\
                    'https://keksik.com.ua{}'.format(product.main_photo.photo.url, )

                for photo_item in product.all_photos:

                    if photo_item.photo.url != product.main_photo.photo.url:
                        # print('1321-213:Photo: %s' % photo_item.photo.url, )
                        # logger.info('1321-213:Photo: %s' % photo_item.photo.url, )

                        etree.SubElement(offer, 'picture').text = \
                            'https://keksik.com.ua{}'.format(photo_item.photo.url, )

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
    logger.info('set_categories(shop) --- {0} seconds --- {1}'.format((time.time() - start_time), len(db.connection.queries), ), )

    db.reset_queries()
    start_time = time.time()
    set_products(shop)
    logger.info('set_products(shop) --- {0} seconds --- {1}'.format((time.time() - start_time), len(db.connection.queries), ), )

    # files = [f for f in os.listdir('.')]
    # for f in files:
    #     logger.info(f)

    with open('/www/projs/prod.keksik_com_ua/storage/yml/prom.ua/shop.yml', 'w') as f:
        f.write(etree.tostring(root).decode('utf-8'))

    stop_datetime = datetime.now()
    logger.info('Stop: generate_prom_ua_yml(*args, **kwargs): datetime.now() {0} | {1}'.format(stop_datetime, (stop_datetime - start_datetime), ), )
    logger.info('Process time: {}'.format(time.time() - start, ), )

    return True, datetime.now(), '__name__: {0}'.format(str(__name__, ), )
