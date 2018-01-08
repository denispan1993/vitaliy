# -*- coding: utf-8 -*-
import email
from celery.utils.log import get_task_logger

from applications.product.models import Product, ItemID
from applications.cart.utils import send_email

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)


def process_import_xml(products_list):
    mismatch_id = 0
    mismatch_id_html = ''
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

        n = 0
        while True:

            try:
                if product_list[n].tag == 'Штрихкод':
                    barcode = product_list[n].text.replace(' ', '', )

                if product_list[n].tag == 'Артикул':
                    itemid = product_list[n].text.replace(' ', '', )

                if product_list[n].tag == 'Наименование':
                    name = product_list[n].text.replace(' ', '', )

            except IndexError:
                break

            n += 1

        if 'itemid' not in locals():
            logger.info('line 113: fix !!! --> product_list[0].tag: %s '
                        'product_list[0].text: %s' % (product_list[0].tag, product_list[0].text, ), )
            without_id += 1
            without_id_html += '{}<br />\n'.format(name if not name == '' else product_list[0].text)
            continue

        try:
            product = ItemID.objects.get(ItemID=itemid, ).parent

            if product.id_1c:

                if product.id_1c != product_list[0].text:
                    """ Не совпадение id 1C между 1C и сайтом """

                    mismatch_id += 1
                    mismatch_id_html += '<br />Артикул: {2} --> {3}|{4}<br />|Site:{0}|1C:{1}|'.\
                        format(product.id_1c, product_list[0].text, itemid, product.title, name, )

                else:
                    if 'barcode' in locals():
                        product.barcode = barcode

            else:
                product.id_1c = product_list[0].text.replace(' ', '', )

            product.save()

            success += 1

        except ItemID.DoesNotExist:
            unsuccess += 1
            unsuccess_itemid_html += '{0} ---> {1}<br />\n'.format(itemid, name, )

        except ItemID.MultipleObjectsReturned:
            double += 1
            double_itemid_html += '{}<br />\n'.format(itemid)

    """ ============================================================================ """
    if without_id:
        send_email(
            subject='Список товаров у которых нету артикулов в 1С.',
            from_email=email.utils.formataddr(('Интернет магазин Keksik', 'site@keksik.com.ua')),
            to_emails=[email.utils.formataddr(('Мэнеджер Интернет магазин Keksik Катерина', 'katerina@keksik.com.ua'), ), ],
            html_content='without_id: {0}<br>\n{1}'.format(without_id, without_id_html, ), )
    """ ============================================================================ """
    if mismatch_id:
        send_email(
            subject='Список товаров у которых при совпадении артикулов, идентификатор 1C не совпадает межу сайтом и 1C.',
            from_email=email.utils.formataddr(('Интернет магазин Keksik', 'site@keksik.com.ua')),
            to_emails=[email.utils.formataddr(('Мэнеджер Интернет магазин Keksik Катерина', 'katerina@keksik.com.ua'), ), ],
            html_content='MisMatch: {0}<br>\n{1}'.format(mismatch_id, mismatch_id_html, ), )
    """ ============================================================================ """
    if unsuccess:
        send_email(
            subject='Список Артикулов которые есть в 1С и которых нету на сайте.',
            from_email=email.utils.formataddr(('Интернет магазин Keksik', 'site@keksik.com.ua')),
            to_emails=[email.utils.formataddr(('Мэнеджер Интернет магазин Keksik Катерина', 'katerina@keksik.com.ua'), ), ],
            html_content='unsuccess: {0}<br>\n{1}'.format(unsuccess, unsuccess_itemid_html, ), )
    """ ============================================================================ """
    if double:
        send_email(
            subject='Список Артикулов которые есть в 1С и которых несколько штук на сайте.',
            from_email=email.utils.formataddr(('Интернет магазин Keksik', 'site@keksik.com.ua')),
            to_emails=[email.utils.formataddr(('Мэнеджер Интернет магазин Keksik Катерина', 'katerina@keksik.com.ua'), ), ],
            html_content='double: {0}<br />\n{1}'.format(double, double_itemid_html, ), )

    '''
        Выбираем товары которые можно сравнивать с 1С (compare_with_1c=True)
        НО у которых нету связки с 1С (id_1c__isnull=True)
    '''
    try:

        # products_ItemID = Product.objects\
        #     .filter(id_1c__isnull=True, compare_with_1c=True, )\
        #     .values_list('ItemID__ItemID', flat=True)

        products = Product.objects\
            .filter(id_1c__isnull=True, compare_with_1c=True, )

        not_found_on_1c = len(products)
        not_found_on_1c_html = ''
        for i, value in enumerate(products, start=1, ):
            not_found_on_1c_html += '{0} ---> {1}<br />\n'.\
                format(value.ItemID.all().first().ItemID, value.title, )

        if not_found_on_1c:
            send_email(
                subject='Список Артикулов которые есть на сайте но нету в 1С.',
                from_email=email.utils.formataddr(('Интернет магазин Keksik', 'site@keksik.com.ua')),
                to_emails=[email.utils.formataddr(('Мэнеджер Интернет магазин Keksik Катерина', 'katerina@keksik.com.ua'), ), ],
                html_content='not_found_on_1c: {0}<br />\n{1}'.format(not_found_on_1c, not_found_on_1c_html, ), )

    except Product.DoesNotExist:
        pass

    try:
        from django.db.models import Q

        q = Q(title__icontains='вафельн') & Q(title__icontains='картинк')
        products = Product.objects.published() \
            .filter(is_availability=1, compare_with_1c=False, ).exclude(q)

        not_compare_with_1c = len(products)
        not_compare_with_1c_html = ''
        for i, value in enumerate(products, start=1, ):
            not_compare_with_1c_html += '{0}: {1} ---> {2}<br />\n'. \
                format(i, value.ItemID.all().first().ItemID, value.title, )

        if not_compare_with_1c:
            send_email(
                subject='Список Артикулов которые есть на сайте но не сравниваются с 1С.',
                from_email=email.utils.formataddr(('Интернет магазин Keksik', 'site@keksik.com.ua')),
                to_emails=[
                    email.utils.formataddr(('Директор Интернет магазин Keksik Светлана', 'lana24680@keksik.com.ua'), ), ],
                html_content='not_compare_with_1c: {0}<br />\n{1}'.format(not_compare_with_1c, not_compare_with_1c_html, ), )

    except Product.DoesNotExist:
        pass
