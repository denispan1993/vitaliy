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

from apps.product.models import ItemID


__author__ = 'AlexStarov'

logger = get_task_logger(__name__)


@celery_app.task()
def process_bitrix_catalog(*args, **kwargs):

    #delivery_pk = kwargs.get('delivery_pk')

    start = time.time()
    path = 'storage/{app}/{year}/{month:02d}/{day:02d}/' \
        .format(
            app='bitrix',
            year=date.today().year,
            month=date.today().month,
            day=date.today().day,
        )

    for name in os.listdir(path, ):
        path_and_filename = os.path.join(path, name)
        if os.path.isfile(path_and_filename, )\
                and name.split('.')[0] == 'import'\
                and name.split('.')[1] == '{hour:02d}'.format(hour=datetime.now().hour, )\
                and name.split('.')[-1] == 'xml':

            root = ET.parse(source=path_and_filename, ).getroot()
            for elem_first_level in root:

                if elem_first_level.tag == u'Каталог':
                    elems_product_level = list(elem_first_level, )

                    if elems_product_level[0].tag == u'Ид' \
                            and elems_product_level[1].tag == u'ИдКлассификатора' \
                            and elems_product_level[2].tag == u'Наименование' \
                            and elems_product_level[3].tag == u'Товары':

                        get_products(list(elems_product_level[3], ), )

    print "Process time: {}".format(time.time() - start, )

    return True, datetime.now(), '__name__: {0}'.format(str(__name__))


def get_products(products_list):
    success = 0
    unsuccess = 0
    unsuccess_itemid = ''
    double = 0
    double_itemid = ''

    for product in products_list:
        product_list = list(product)
        itemid = product_list[1].text
        print(itemid, len(itemid))

        try:
            itemid = ItemID.objects.get(ItemID=product_list[1].text.replace(' ', '',), )  # using('real').
            product = itemid.parent
            product.id_1c = product_list[0].text
            product.save()

            success += 1
            print(success, ': ', u'Артикул:-->"', product_list[1].text.replace(' ', '',), '"<--:Found', )

        except ItemID.DoesNotExist:
            unsuccess += 1
            unsuccess_itemid += '%s<br /> \n' % product_list[1].text.replace(' ', '',)
            print(unsuccess, ': ', u'Артикул:-->"', product_list[1].text.replace(' ', '',), '"<--:Not Found', )

        except ItemID.MultipleObjectsReturned:
            double += 1
            double_itemid += '%s<br /> \n' % product_list[1].text.replace(' ', '',)
            print(double, ': ', u'Артикул:-->"', product_list[1].text.replace(' ', '',), '"<--:Double', )

    print('success: ', success)
    print('unsuccess: ', unsuccess)
    print(unsuccess_itemid)
    print('double: ', double)
    print(double_itemid)

    backend = smtp.EmailBackend(
        host='smtp.yandex.ru',
        port=465,
        username='site@keksik.com.ua',
        password='1q2w3e4r',
        use_tls=False,
        fail_silently=False,
        use_ssl=True,
        timeout=30,
        ssl_keyfile=None,
        ssl_certfile=None, )

    msg = EmailMultiAlternatives(
        subject=u'Список Артикулов которые есть в 1С и которых нету на сайте.',
        body=strip_tags(unsuccess_itemid, ),
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
        connection=backend, )

    msg.attach_alternative(content=u'unsuccess: {0}<br> {1}'.format(unsuccess, unsuccess_itemid, ),
                           mimetype="text/html", )

    msg.content_subtype = "html"
    i = 0
    while True:
        result = msg.send(fail_silently=False, )

        if (isinstance(result, int) and result == 1) or i > 100:
            i = 0
            break

        print('bitrix.tasks.process_bitrx_catalog.unsuccess(i): ', i, ' result: ', result,)
        i += 1
        time.sleep(5)

    msg = EmailMultiAlternatives(
        subject=u'Список Артикулов которые есть в 1С и которых несколько штук на сайте.',
        body=strip_tags(double_itemid, ),
        from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
        to=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
        connection=backend, )

    msg.attach_alternative(content=u'double: {0}<br /> {1}'.format(double, double_itemid, ),
                           mimetype="text/html", )

    msg.content_subtype = "html"
    i = 0
    while True:
        result = msg.send(fail_silently=False, )

        if (isinstance(result, int) and result == 1) or i > 100:
            i = 0
            break

        print('bitrix.tasks.process_bitrx_catalog.double(i): ', i, ' result: ', result,)
        i += 1
        time.sleep(5)
