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

from apps.product.models import Product, ItemID


__author__ = 'AlexStarov'

logger = get_task_logger(__name__)


@celery_app.task()
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

    print "Process time: {}".format(time.time() - start, )

    return True, datetime.now(), '__name__: {0}'.format(str(__name__))


def get_products(products_list):
    success = 0
    unsuccess = 0
    unsuccess_itemid_html = ''
    double = 0
    double_itemid_html = ''

    for product in products_list:
        product_list = list(product)

        if 'itemid' in locals():
            del(itemid)
        if 'barcode' in locals():
            del(barcode)

        for n in xrange(5):

            try:
                if product_list[n].tag == u'Штрихкод':
                    barcode = product_list[n].text.replace(' ', '', )
                if product_list[n].tag == u'Артикул':
                    itemid = product_list[n].text.replace(' ', '', )
                    break
            except IndexError:
                break
        else:
            print('line 87: fix !!! --> product_list[0].tag:  ', product_list[0].tag, ' product_list[0].text: ', product_list[0].text)
            continue

        if 'itemid' not in locals():
            print('line 91: fix !!! --> product_list[0].tag:  ', product_list[0].tag, ' product_list[0].text: ', product_list[0].text)
            continue

        #print(itemid, len(itemid))

        try:
            product = ItemID.objects.get(ItemID=itemid, ).parent  # using('real').

            if product.id_1c:

                if product.id_1c != product_list[0].text:
                    print('line 102: fix !!! --> product.id_1c: ', product.id_1c,
                          ' --> product_list[0].text: ', product_list[0].text)
                else:
                    if 'barcode' in locals():
                        product.barcode = barcode

            else:
                product.id_1c = product_list[0].text.replace(' ', '', )

            product.save()

            success += 1
            #print(success, ': ', u'Артикул:-->"', itemid, '"<--:Found', )

        except ItemID.DoesNotExist:
            unsuccess += 1
            unsuccess_itemid_html += '%s<br /> \n' % itemid
            #print(unsuccess, ': ', u'Артикул:-->"', itemid, '"<--:Not Found', )

        except ItemID.MultipleObjectsReturned:
            double += 1
            double_itemid_html += '%s<br /> \n' % itemid
            #print(double, ': ', u'Артикул:-->"', itemid, '"<--:Double', )

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

    msg = EmailMultiAlternatives(
        subject=u'Список Артикулов которые есть в 1С и которых нету на сайте.',
        body=strip_tags(unsuccess_itemid_html, ),
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
        connection=backend, )

    msg.attach_alternative(content=u'unsuccess: {0}<br> {1}'.format(unsuccess, unsuccess_itemid_html, ),
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

    msg = EmailMultiAlternatives(
        subject=u'Список Артикулов которые есть в 1С и которых несколько штук на сайте.',
        body=strip_tags(double_itemid_html, ),
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
        connection=backend, )

    msg.attach_alternative(content=u'double: {0}<br /> {1}'.format(double, double_itemid_html, ),
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

    try:
        products_ItemID = Product.objects\
            .filter(id_1c__isnull=True, )\
            .values_list('ItemID__ItemID', flat=True)

        not_found_on_1c = len(products_ItemID)
        not_found_on_1c_html = '<br />'.join(products_ItemID)

    except Product.DoesNotExist:
        pass

    msg = EmailMultiAlternatives(
        subject=u'Список Артикулов которые есть на сайте но нету в 1С.',
        body=strip_tags(not_found_on_1c_html, ),
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
        connection=backend, )

    msg.attach_alternative(content=u'not_found_on_1c: {0}<br /> {1}'.format(not_found_on_1c, not_found_on_1c_html, ),
                           mimetype="text/html", )

    msg.content_subtype = "html"
    i = 0
    while True:
        result = msg.send(fail_silently=False, )

        if (isinstance(result, int) and result == 1) or i > 100:
            break

        print('bitrix.tasks.process_bitrx_catalog.not_found_on_1c(i): ', i, ' result: ', result,)
        i += 1
        time.sleep(5)

    print('success: ', success)
    print('unsuccess: ', unsuccess)
    print('double: ', double)
    print('not_found_on_1c: ', not_found_on_1c)


def process_of_proposal(offers_list):

    success = 0
    there_is_in_1c = ''
    there_is_in_site = ''

    for offer in offers_list:
        offer_list = list(offer)

        if 'id_1c' in locals():
            del(id_1c)

        n = 0
        while True:

            try:
                if offer_list[n].tag == u'Ид':
                    id_1c = offer_list[n].text.replace(' ', '', )

                if offer_list[n].tag == u'Количество':
                    quantity_of_stock = offer_list[n].text.replace(' ', '', )

            except IndexError:
                break

            n += 1

        if 'id_1c' not in locals():
            print('line 267: fix !!! --> offer_list[0].tag:  ', offer_list[0].tag,
                  ' offer_list[0].text: ', offer_list[0].text)
            continue

        if 'quantity_of_stock' in locals():
            try:
                quantity_of_stock = int(quantity_of_stock)

            except ValueError:
                print('line 276: fix !!! --> offer_list[0].tag:  ', offer_list[0].tag,
                      ' offer_list[0].text: ', offer_list[0].text)
                continue
        else:
            print('line 280: fix !!! --> offer_list[0].tag:  ', offer_list[0].tag,
                  ' offer_list[0].text: ', offer_list[0].text)

        try:
            product = Product.objects.get(id_1c=id_1c, )

            if quantity_of_stock > 0 and product.is_availability == 1:
                product.quantity_of_stock = quantity_of_stock
                product.save()

            if quantity_of_stock > 0 and product.is_availability != 1:
                there_is_in_1c += u'{}<br />'.format(product.ItemID.all()[0].ItemID)

            if quantity_of_stock == 0 and product.is_availability == 1:
                there_is_in_site += u'{}<br />'.format(product.ItemID.all()[0].ItemID)

            success += 1
            # print(success, ': ', u'Артикул:-->"', itemid, '"<--:Found', )

        except Product.DoesNotExist:
            pass

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

    msg = EmailMultiAlternatives(
        subject=u'Список Артикулов продукты которые есть в 1С и отсутствуют на сайте.',
        body=strip_tags(there_is_in_1c, ),
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
        connection=backend, )

    msg.attach_alternative(content=u'{0}'.format(there_is_in_1c, ),
                           mimetype="text/html", )

    msg.content_subtype = "html"
    i = 0
    while True:
        result = msg.send(fail_silently=False, )

        if (isinstance(result, int) and result == 1) or i > 100:
            break

        print('bitrix.tasks.process_bitrx_catalog.there_is_in_1c(i): ', i, ' result: ', result,)
        i += 1
        time.sleep(5)

    msg = EmailMultiAlternatives(
        subject=u'Список Артикулов продукты которые есть на сайте но отсутствуют в 1С.',
        body=strip_tags(there_is_in_site, ),
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
        connection=backend, )

    msg.attach_alternative(content=u'{0}'.format(there_is_in_site, ),
                           mimetype="text/html", )

    msg.content_subtype = "html"
    i = 0
    while True:
        result = msg.send(fail_silently=False, )

        if (isinstance(result, int) and result == 1) or i > 100:
            break

        print('bitrix.tasks.process_bitrx_catalog.there_is_in_site(i): ', i, ' result: ', result,)
        i += 1
        time.sleep(5)
