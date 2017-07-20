# -*- coding: utf-8 -*-
import os
import time
import email
from datetime import datetime, date
import xml.etree.ElementTree as ET
from django.core.mail.backends import smtp
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from celery.utils.log import get_task_logger
from proj.celery import celery_app

from applications.product.models import Product, ItemID
from applications.cart.utils import send_email

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)

backend = smtp.EmailBackend(
    host='smtp.yandex.ru',
    port=465,
    username='site@keksik.com.ua',
    password='1q2w3e4r!!!@@@',
    use_tls=False,
    fail_silently=False,
    use_ssl=True,
    timeout=30,
    ssl_keyfile=None,
    ssl_certfile=None, )


def decorate(func):
    # start = time.time()
    # print(u'Декорируем %s(*args, **kwargs): | Start: %s' % (func.__name__, start, ), )
    # logger.info(u'Декорируем %s... | Start: %s' % (func.__name__, start, ), )

    def wrapped(*args, **kwargs):
        start = time.time()
        print(u'Декорируем %s(*args, **kwargs): | Start: %s' % (func.__name__, start,), )
        logger.info(u'Декорируем %s... | Start: %s' % (func.__name__, start,), )

        print(u'Вызываем обёрнутую функцию с аргументами: *args, **kwargs', )
        logger.info(u'Вызываем обёрнутую функцию с аргументами: *args, **kwargs', )
        result = func(*args, **kwargs)

        stop = time.time()
        print(u'выполнено! | Stop: %s | Running time: %s' % (stop, stop - start, ), )
        logger.info(u'выполнено! | Stop: %s | Running time: %s' % (stop, stop - start, ), )

        return result

    # stop = time.time()
    # print(u'выполнено! | Stop: %s | Running time: %s' % (stop, stop - start, ), )
    # logger.info(u'выполнено! | Stop: %s | Running time: %s' % (stop, stop - start, ), )

    return wrapped


@celery_app.task()
@decorate
def process_bitrix_catalog(*args, **kwargs):

    start = time.time()

    year = date.today().year
    month = date.today().month
    day = date.today().day
    hour = datetime.now().hour

    path = 'storage/{app}/{year}/{month:02d}/{day:02d}/' \
        .format(
            app='bitrix',
            year=year,
            month=month,
            day=day,
        )

    for name in os.listdir(path, ):
        path_and_filename = os.path.join(path, name)

        if os.path.isfile(path_and_filename, )\
                and name.split('.')[0] == 'import'\
                and name.split('.')[1] == '{hour:02d}'.format(hour=hour, )\
                and name.split('.')[-1] == 'xml':

            root = ET.parse(source=path_and_filename, ).getroot()
            for elem_first_level in root:

                if elem_first_level.tag == u'Каталог':

                    elems_product_level = list(elem_first_level, )

                    if elems_product_level[0].tag == u'Ид' \
                            and elems_product_level[1].tag == u'ИдКлассификатора' \
                            and elems_product_level[2].tag == u'Наименование' \
                            and elems_product_level[3].tag == u'Владелец'\
                            and elems_product_level[4].tag == u'Товары':

                        get_products(list(elems_product_level[4], ), )

    for name in os.listdir(path, ):
        path_and_filename = os.path.join(path, name)

        if os.path.isfile(path_and_filename, )\
                and name.split('.')[0] == 'offers'\
                and name.split('.')[1] == '{hour:02d}'.format(hour=hour, )\
                and name.split('.')[-1] == 'xml':

            root = ET.parse(source=path_and_filename, ).getroot()
            level1 = list(root[0])
            for elem_second_level in level1:

                if elem_second_level.tag == u'Предложения':

                    process_of_proposal(offers_list=list(elem_second_level, ), )

    logger.info('Process time: {}'.format(time.time() - start, ), )

    return True, datetime.now(), '__name__: {0}'.format(str(__name__, ), )


def get_products(products_list):
    success = 0
    unsuccess = 0
    unsuccess_itemid_html = ''
    double = 0
    double_itemid_html = ''
    without_id = 0
    without_id_html = ''

    for product in products_list:
        product_list = list(product)

        if 'itemid' in locals():
            del(itemid)
        if 'barcode' in locals():
            del(barcode)

        for n in range(5):

            try:
                if product_list[n].tag == u'Штрихкод':
                    barcode = product_list[n].text.replace(' ', '', )
                if product_list[n].tag == u'Артикул':
                    itemid = product_list[n].text.replace(' ', '', )
                    break
            except IndexError:
                break
        else:
            """ Если цикл закончился не по break а просто вышел то тогда срабоатывает else """
            logger.info('line 109: without Artikul fix !!! --> product_list[0].tag: %s '
                        'product_list[0].text: %s' % (product_list[0].tag, product_list[0].text, ), )

            name = ''
            for n in range(6):
                """ Ищем 'Наименование' товара """
                try:
                    if product_list[n].tag == u'Наименование':
                        name = product_list[n].text
                        break
                except IndexError:
                    break
            without_id += 1
            without_id_html += u'{}<br />\n'.format(name if not name == '' else product_list[0].text)
            continue

        if 'itemid' not in locals():
            logger.info('line 113: fix !!! --> product_list[0].tag: %s '
                        'product_list[0].text: %s' % (product_list[0].tag, product_list[0].text, ), )
            continue

        try:
            product = ItemID.objects.get(ItemID=itemid, ).parent  # using('real').

            if product.id_1c:

                if product.id_1c != product_list[0].text:
                    logger.info('line 124: fix !!! --> product.id_1c: %s  --> '
                                'product_list[0].text:  %s' % (product.id_1c, product_list[0].text, ), )
                else:
                    if 'barcode' in locals():
                        product.barcode = barcode

            else:
                product.id_1c = product_list[0].text.replace(' ', '', )

            product.save()

            success += 1

        except ItemID.DoesNotExist:
            unsuccess += 1
            unsuccess_itemid_html += u'{}<br />\n'.format(itemid)

        except ItemID.MultipleObjectsReturned:
            double += 1
            double_itemid_html += u'{}<br />\n'.format(itemid)

    """ ============================================================================ """
    msg = EmailMultiAlternatives(
        subject=u'Список товаров у которых нету артикулов в 1С.',
        body=strip_tags(without_id_html, ),
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
        connection=backend, )

    msg.attach_alternative(content=u'unsuccess: {0}<br>\n{1}'.format(without_id, without_id_html, ),
                           mimetype="text/html", )

    msg.content_subtype = "html"
    i = 0
    while True:
        result = msg.send(fail_silently=False, )

        if (isinstance(result, int) and result == 1) or i > 100:
            break

        print('bitrix.tasks.process_bitrx_catalog.unsuccess(i): ', i, ' result: ', result,)
        i += 1
        time.sleep(5)

    """ ============================================================================ """
    msg = EmailMultiAlternatives(
        subject=u'Список Артикулов которые есть в 1С и которых нету на сайте.',
        body=strip_tags(unsuccess_itemid_html, ),
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
        connection=backend, )

    msg.attach_alternative(content=u'unsuccess: {0}<br>\n{1}'.format(unsuccess, unsuccess_itemid_html, ),
                           mimetype="text/html", )

    msg.content_subtype = "html"
    i = 0
    while True:
        result = msg.send(fail_silently=False, )

        if (isinstance(result, int) and result == 1) or i > 100:
            break

        print('bitrix.tasks.process_bitrx_catalog.unsuccess(i): ', i, ' result: ', result,)
        i += 1
        time.sleep(5)

    """ ============================================================================ """
    msg = EmailMultiAlternatives(
        subject=u'Список Артикулов которые есть в 1С и которых несколько штук на сайте.',
        body=strip_tags(double_itemid_html, ),
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
        connection=backend, )

    msg.attach_alternative(content=u'double: {0}<br />\n{1}'.format(double, double_itemid_html, ),
                           mimetype="text/html", )

    msg.content_subtype = "html"
    i = 0
    while True:
        result = msg.send(fail_silently=False, )

        if (isinstance(result, int) and result == 1) or i > 100:
            break

        print('bitrix.tasks.process_bitrx_catalog.double(i): ', i, ' result: ', result,)
        i += 1
        time.sleep(5)

    '''
        Выбираем товары которые можно сравнивать с 1С (compare_with_1c=True)
        НО у которых нету связки с 1С (id_1c__isnull=True)
    '''
    try:
        products_ItemID = Product.objects\
            .filter(id_1c__isnull=True, compare_with_1c=True, )\
            .values_list('ItemID__ItemID', flat=True)

        not_found_on_1c = len(products_ItemID)
        not_found_on_1c_html = u'<br />\n'.join(products_ItemID)

        msg = EmailMultiAlternatives(
            subject=u'Список Артикулов которые есть на сайте но нету в 1С.',
            body=strip_tags(not_found_on_1c_html, ),
            from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
            to=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
            connection=backend, )
        msg.attach_alternative(content=u'not_found_on_1c: {0}<br />\n{1}'.format(not_found_on_1c, not_found_on_1c_html, ),
                               mimetype="text/html", )
        msg.content_subtype = "html"
        i = 0

        while True:
            result = msg.send(fail_silently=False, )
            if (isinstance(result, int) and result == 1) or i > 100:
                break
            print('bitrix.tasks.process_bitrx_catalog.not_found_on_1c(i): ', i, ' result: ', result, )
            i += 1
            time.sleep(5)

    except Product.DoesNotExist:
        pass


def process_of_proposal(offers_list):

    success = 0
    there_is_in_1c = 0
    there_is_in_1c_html = ''
    there_is_in_site = 0
    there_is_in_site_html = ''

    for offer in offers_list:
        offer_list = list(offer)

        if 'id_1c' in locals():
            del(id_1c, )

        n = 0
        while True:

            try:
                if offer_list[n].tag == u'Ид':
                    id_1c = offer_list[n].text.replace(' ', '', )

                if offer_list[n].tag == u'Количество':
                    quantity_of_stock = offer_list[n].text.replace(' ', '', )

                if offer_list[n].tag == u'Цены':
                    price = get_price(prices=list(offer_list[n]))

            except IndexError:
                break

            n += 1

        if 'id_1c' not in locals():
            logger.info('line 277: fix 1!!! --> offer_list[0].tag: {0} | offer_list[0].text: {1}'\
                        .format(offer_list[0].tag, offer_list[0].text, ), )
            continue

        if 'quantity_of_stock' in locals():
            try:
                quantity_of_stock = int(quantity_of_stock)

            except ValueError:
                logger.info('line 286: fix 2!!! --> offer_list[0].tag: {0} |  offer_list[0].text: {1}'\
                            .format(offer_list[0].tag, offer_list[0].text, ), )
                continue
        else:
            logger.info('line 290: fix 3!!! --> offer_list[0].tag: {0} | offer_list[0].text: {1}'\
                        .format(offer_list[0].tag, offer_list[0].text, ), )

        try:
            product = Product.objects.get(id_1c=id_1c, )

            ''' Если в 1С единиц товара больше чем 0 и в базе сайта он "в наличии"
                то просто записывеем количество товара в базу сайта '''
            if quantity_of_stock > 0 and product.is_availability == 1:
                product.quantity_of_stock = quantity_of_stock
                product.save()

            if quantity_of_stock > 0 and product.is_availability != 1:
                there_is_in_1c += 1
                there_is_in_1c_html += u'{}: {}<br />\n'.format(product.ItemID.all()[0].ItemID, product.title)

            if quantity_of_stock == 0 and product.is_availability == 1:
                there_is_in_site += 1
                there_is_in_site_html += u'{}: {}<br />\n'.format(product.ItemID.all()[0].ItemID, product.title)

            success += 1
            # print(success, ': ', u'Артикул:-->"', itemid, '"<--:Found', )

        except Product.DoesNotExist:
            pass

        except Product.MultipleObjectsReturned:
            products = Product.objects.filter(id_1c=id_1c, )
            for product in products:
                logger.info('line 321: fix 4!!! -->: {0} | {1} | {2}'\
                            .format(product, product.ItemID.all()[0].ItemID, product.title, ), )

    """ ============================================================================ """
    send_email(
        subject=u'Список Артикулов товаров которые есть в 1С но отсутствуют на сайте.',
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to_emails=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
        html_content=u'{0}<br />\n{1}'.format(there_is_in_1c, there_is_in_1c_html), )

    """ ============================================================================ """
    send_email(
        subject=u'Список Артикулов товаров которые есть на сайте но отсутствуют в 1С.',
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to_emails=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
        html_content=u'{0}<br />\n{1}'.format(there_is_in_site, there_is_in_site_html), )

    """ ============================================================================ """
    send_email(
        subject=u'Список Артикулов товаров которые есть на сайте но отсутствуют в 1С.',
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to_emails=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Виктория', u'zakaz@keksik.com.ua'), ), ],
        html_content=u'{0}<br />\n{1}'.format(there_is_in_site, there_is_in_site_html), )


def get_price(prices):
    found_price_1c_id = False
    i = 0
    while True:
        price = list(prices[i])
        i += 1
        n = 0
        while True:
            if price[n].tag == 'ИдТипаЦены':
                if price[n].text.replace(' ', '', ) == 'ea0d32d8-abdf-11e5-8023-000c29aa1c5b':
                    found_price_1c_id = True
                else:
                    break
            if price[n].tag == 'ЦенаЗаЕдиницу' and found_price_1c_id:
                return price[n].text.replace(' ', '', )

            n += 1

    return None
