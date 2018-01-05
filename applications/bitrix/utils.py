# -*- coding: utf-8 -*-
import email
import re
from celery.utils.log import get_task_logger

from applications.product.models import Product, ItemID
from applications.cart.utils import send_email

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)


def get_products(products_list):
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

        for n in range(5):

            try:
                if product_list[n].tag == 'Штрихкод':
                    barcode = product_list[n].text.replace(' ', '', )
                if product_list[n].tag == 'Артикул':
                    itemid = product_list[n].text.replace(' ', '', )
                    if product_list[n+1].tag == 'Наименование':
                        name = product_list[n+1].text.replace(' ', '', )
                    else:
                        name = None
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
                    if product_list[n].tag == 'Наименование':
                        name = product_list[n].text
                        break
                except IndexError:
                    break
            without_id += 1
            without_id_html += '{}<br />\n'.format(name if not name == '' else product_list[0].text)
            continue

        if 'itemid' not in locals():
            logger.info('line 113: fix !!! --> product_list[0].tag: %s '
                        'product_list[0].text: %s' % (product_list[0].tag, product_list[0].text, ), )
            continue

        try:
            product = ItemID.objects.get(ItemID=itemid, ).parent  # using('real').

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
    if mismatch_id:
        send_email(
            subject='Список товаров у которых при совпадении артикулов, идентификатор 1C не совпадает межу сайтом и 1C.',
            from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
            to_emails=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
            html_content='MisMatch: {0}<br>\n{1}'.format(mismatch_id, mismatch_id_html, ), )
    """ ============================================================================ """
    if without_id:
        send_email(
            subject='Список товаров у которых нету артикулов в 1С.',
            from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
            to_emails=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
            html_content='without_id: {0}<br>\n{1}'.format(without_id, without_id_html, ), )
    """ ============================================================================ """
    if unsuccess:
        send_email(
            subject='Список Артикулов которые есть в 1С и которых нету на сайте.',
            from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
            to_emails=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
            html_content='unsuccess: {0}<br>\n{1}'.format(unsuccess, unsuccess_itemid_html, ), )
    """ ============================================================================ """
    if double:
        send_email(
            subject='Список Артикулов которые есть в 1С и которых несколько штук на сайте.',
            from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
            to_emails=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
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
                from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
                to_emails=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
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
                from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
                to_emails=[
                    email.utils.formataddr((u'Директор Интернет магазин Keksik Светлана', u'lana24680@keksik.com.ua'), ), ],
                html_content='not_compare_with_1c: {0}<br />\n{1}'.format(not_compare_with_1c, not_compare_with_1c_html, ), )

    except Product.DoesNotExist:
        pass


def process_of_proposal(offers_list):

    there_is_in_1c = 0
    there_is_in_1c_html = ''
    there_is_in_site = 0
    there_is_in_site_html = ''
    discrepancy_price = 0
    discrepancy_price_html = ''
    currency_discrepancy = 0
    currency_discrepancy_html = ''

    for offer in offers_list:
        offer_list = list(offer)

        if 'id_1c' in locals():
            del(id_1c, )

        n = 0
        while True:

            try:
                if offer_list[n].tag == 'Ид':
                    id_1c = offer_list[n].text.replace(' ', '', )

                if offer_list[n].tag == 'Количество':
                    quantity_in_stock = offer_list[n].text.replace(' ', '', )

                if offer_list[n].tag == 'Цены':
                    price = get_price(prices=list(offer_list[n]))
                    # logger.info('line 331: fix 5!!! --> price: {0} | id_1c: {1}'.
                    #             format(price, id_1c, ), )

            except IndexError:
                break

            n += 1

        if 'id_1c' not in locals():
            logger.info('line 277: fix 1!!! --> offer_list[0].tag: {0} | offer_list[0].text: {1}'\
                        .format(offer_list[0].tag, offer_list[0].text, ), )
            continue

        if 'quantity_in_stock' in locals():
            try:
                quantity_in_stock = int(quantity_in_stock)

            except ValueError:
                logger.info('line 286: fix 2!!! --> offer_list[0].tag: {0} |  offer_list[0].text: {1}'\
                            .format(offer_list[0].tag, offer_list[0].text, ), )
                continue
        else:
            logger.info('line 290: fix 3!!! --> offer_list[0].tag: {0} | offer_list[0].text: {1}'\
                        .format(offer_list[0].tag, offer_list[0].text, ), )

        try:
            product = Product.objects.get(id_1c=id_1c, )

            if quantity_in_stock > 0 and product.is_availability == 1:
                """ Если в 1С единиц товара больше чем 0 и в базе сайта он "в наличии" """
                product.quantity_in_stock = quantity_in_stock
                """ то просто записывеем количество товара в базу сайта """
                product.save()

            elif quantity_in_stock > 0 and product.is_availability != 1:
                """ Количество товара в 1С > 0 но отсутствуют на сайте. """
                there_is_in_1c += 1
                there_is_in_1c_html += '{}: {}<br />\n'.format(product.ItemID.all()[0].ItemID, product.title)
                """ то записывеем количество товара в базу сайта """
                product.quantity_in_stock = quantity_in_stock
                """ меняем товар на "в наличии" """
                product.is_availability = 1
                product.save()

            elif quantity_in_stock == 0 and product.is_availability == 1:
                """ товар "есть" на сайте но в 1С остатки < 0 """
                there_is_in_site += 1
                there_is_in_site_html += '{}: {}<br />\n'.format(product.ItemID.all()[0].ItemID, product.title)
                """ то обнуляем количество товара в базе сайта """
                product.quantity_in_stock = 0

                if 'резак' in product.title and \
                    (product.ItemID.all()[0].ItemID.startwith('og', re.I) or
                     product.ItemID.all()[0].ItemID.startwith('ra', re.I) or
                     product.ItemID.all()[0].ItemID.startwith('rn', re.I)):

                    product.is_availability = 2
                else:

                    # TODO: ожидается ли?
                    """ меняем наличие товара на "ожидается" """
                    product.is_availability = 3

                product.save()

            if product.is_active \
                    and product.visibility \
                    and product.is_availability == 1:

                ''' Сравнение цен '''  # '%.2f' % 1.234  |  "{0:.2f}".format(5)
                try:
                    price_1C = '{0:.2f}'.format(float(price.get(product.currency.currency_code_ISO_char, ), ), )
                    price_site = '{0:.2f}'.format(product.price)

                    if price_1C != price_site:

                        discrepancy_price += 1
                        discrepancy_price_html += '{}: {}<br />\n'.format(product.ItemID.all()[0].ItemID, product.title, )

                except TypeError:
                    """ Если не сходятся валюта товара между сайтом и 1С. """
                    currency_discrepancy += 1
                    currency_discrepancy_html += '{0}: {1} | {2}<br />\n'.format(product.ItemID.all()[0].ItemID, product.title, price, )

                    # logger.info('line 377: fix 4!!! --> price: {0} | ItemID: {1} | id_1c: {2}'.
                    #             format(price, product.ItemID.all()[0].ItemID, id_1c, ), )

        except Product.DoesNotExist:
            pass

        except Product.MultipleObjectsReturned:
            products = Product.objects.filter(id_1c=id_1c, )
            for product in products:
                logger.info('line 321: fix 4!!! -->: {0} | {1} | {2}'\
                            .format(product, product.ItemID.all()[0].ItemID, product.title, ), )

    """ ============================================================================ """
    if there_is_in_1c:
        send_email(
            subject='Список Артикулов товаров остатки которых в 1С > 0, НО на сайте значатся как отсутсвующие.',
            from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
            to_emails=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ), ],
            html_content='{0}<br />\n{1}'.format(there_is_in_1c, there_is_in_1c_html), )

    """ ============================================================================ """
    if there_is_in_site:
        send_email(
            subject='Список Артикулов товаров остатки которых есть на сайте, НО в 1С значатся как закончившиеся.',
            from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
            to_emails=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ),
                       email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'zakaz@keksik.com.ua'), ),],
            html_content='{0}<br />\n{1}'.format(there_is_in_site, there_is_in_site_html), )

    """ ============================================================================ """
    if currency_discrepancy:
        send_email(
            subject='Список Артикулов товаров которые расходятся по ВАЛЮТАМ с 1С.',
            from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
            to_emails=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ),
                       email.utils.formataddr((u'Директор Интернет магазин Keksik Светлана Витальевна', u'lana24680@keksik.com.ua'), ), ],
            html_content='currency_discrepancy: {0}<br />\n{1}'.format(currency_discrepancy, currency_discrepancy_html), )

    """ ============================================================================ """
    if discrepancy_price:
        send_email(
            subject='Список Артикулов товаров которые расходятся по ценам с 1С.',
            from_email=email.utils.formataddr((u'Интернет магазин Keksik', u'site@keksik.com.ua')),
            to_emails=[email.utils.formataddr((u'Мэнеджер Интернет магазин Keksik Катерина', u'katerina@keksik.com.ua'), ),
                       email.utils.formataddr((u'Директор Интернет магазин Keksik Светлана Витальевна', u'lana24680@keksik.com.ua'), ), ],
            html_content='discrepancy_price: {0}<br />\n{1}'.format(discrepancy_price, discrepancy_price_html), )


def get_price(prices: list) -> dict:
    """
        return the price dictionary in the found currency positions
    :param prices: list -> XML List
    :return: dict -> price dict with key currency
    """
    logger.info('line 427: fix 6!!! -->: {0}'.format(prices, ), )
    found_price_1c_id_UAH = False
    found_price_1c_id_USD = False
    price_dict = {}
    i = 0
    while True:
        try:
            price = list(prices[i])
            logger.info('line 435: fix 7!!! -->: {0}'.format(price, ), )
        except IndexError:
            return price_dict

        i += 1
        n = 0
        while True:
            try:
                item = price[n]
                logger.info('line 444: fix 8!!! -->: item: {0}'.format(item, ), )
            except IndexError:
                break

            logger.info('line 447: fix 9!!! item.tag -->: type: {0} | {1} | item.text -->: type: {2} | {3}'
                        .format(type(item.tag), item.tag, type(item.text), item.text, ), )
            if item.tag == 'ИдТипаЦены':
                # Отпускная цена
                if item.text.replace(' ', '', ) == '3cf4bfc9-dae5-11e6-aa20-d9c641a3a917':
                    found_price_1c_id_UAH = True
                    found_price_1c_id_USD = False
                # Отпускная цена $
                elif item.text.replace(' ', '', ) == '3cf4bfca-dae5-11e6-aa20-d9c641a3a917':
                    found_price_1c_id_USD = True
                    found_price_1c_id_UAH = False

            if price[n].tag == 'ЦенаЗаЕдиницу':
                if found_price_1c_id_UAH:
                    price_dict.update({'UAH': price[n].text.replace(' ', '', ), }, )
                    found_price_1c_id_UAH = False

                if found_price_1c_id_USD:
                    price_dict.update({'USD': price[n].text.replace(' ', '', ), }, )
                    found_price_1c_id_USD = False

            n += 1
