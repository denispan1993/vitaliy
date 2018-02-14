# -*- coding: utf-8 -*-
import email
import re
from celery.utils.log import get_task_logger

from applications.product.models import Product
from applications.cart.utils import send_email

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)


def process_offers_xml(offers_list):

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

            except IndexError:
                break

            n += 1

        if 'id_1c' not in locals():
            logger.info('line 277: fix 1!!! --> offer_list[0].tag: {tag} | offer_list[0].text: {text}'\
                        .format(tag=offer_list[0].tag, text=offer_list[0].text, ), )
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
            ItemID = product.ItemID.all()[0].ItemID

            if quantity_in_stock > 0 and product.is_availability == 1:
                """ Если в 1С единиц товара больше чем 0 и в базе сайта он "в наличии" """
                product.quantity_in_stock = quantity_in_stock
                """ то просто записывеем количество товара в базу сайта """
                product.save()

            elif quantity_in_stock > 0 and product.is_availability != 1:
                """ Количество товара в 1С > 0 но отсутствуют на сайте. """
                there_is_in_1c += 1
                there_is_in_1c_html += '{}: {}<br />\n'.format(ItemID, product.title)
                """ то записывеем количество товара в базу сайта """
                product.quantity_in_stock = quantity_in_stock
                """ меняем товар на "в наличии" """
                product.is_availability = 1
                product.save()

            elif quantity_in_stock == 0 and product.is_availability == 1:
                """ товар "есть" на сайте но в 1С остатки < 0 """
                there_is_in_site += 1
                there_is_in_site_html += '{}: {}<br />\n'.format(ItemID, product.title)
                """ то обнуляем количество товара в базе сайта """
                product.quantity_in_stock = 0

                if 'резак' in product.title and \
                    (ItemID.startswith('og', re.I) or
                     ItemID.startswith('ra', re.I) or
                     ItemID.startswith('rn', re.I)):

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
                        discrepancy_price_html += '{}: {}<br />\n'.format(ItemID, product.title, )

                except TypeError:
                    """ Если не сходятся валюта товара между сайтом и 1С. """
                    currency_discrepancy += 1
                    currency_discrepancy_html += '{0}: {1} | {2}<br />\n'.format(ItemID, product.title, price, )

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
            from_email=email.utils.formataddr(('Интернет магазин Keksik', 'site@keksik.com.ua')),
            to_emails=[email.utils.formataddr(('Мэнеджер Интернет магазин Keksik Катерина', 'katerina@keksik.com.ua'), ), ],
            html_content='{0}<br />\n{1}'.format(there_is_in_1c, there_is_in_1c_html), )

    """ ============================================================================ """
    if there_is_in_site:
        send_email(
            subject='Список Артикулов товаров остатки которых есть на сайте, НО в 1С значатся как закончившиеся.',
            from_email=email.utils.formataddr(('Интернет магазин Keksik', 'site@keksik.com.ua')),
            to_emails=[email.utils.formataddr(('Мэнеджер Интернет магазин Keksik Катерина', 'katerina@keksik.com.ua'), ),
                       email.utils.formataddr(('Мэнеджер Интернет магазин Keksik Катерина', 'zakaz@keksik.com.ua'), ),],
            html_content='{0}<br />\n{1}'.format(there_is_in_site, there_is_in_site_html), )

    """ ============================================================================ """
    if currency_discrepancy:
        send_email(
            subject='Список Артикулов товаров которые расходятся по ВАЛЮТАМ с 1С.',
            from_email=email.utils.formataddr(('Интернет магазин Keksik', 'site@keksik.com.ua')),
            to_emails=[email.utils.formataddr(('Мэнеджер Интернет магазин Keksik Катерина', 'katerina@keksik.com.ua'), ),
                       email.utils.formataddr(('Директор Интернет магазин Keksik Светлана Витальевна', 'lana24680@keksik.com.ua'), ), ],
            html_content='currency_discrepancy: {0}<br />\n{1}'.format(currency_discrepancy, currency_discrepancy_html), )

    """ ============================================================================ """
    if discrepancy_price:
        send_email(
            subject='Список Артикулов товаров которые расходятся по ценам с 1С.',
            from_email=email.utils.formataddr(('Интернет магазин Keksik', 'site@keksik.com.ua')),
            to_emails=[email.utils.formataddr(('Мэнеджер Интернет магазин Keksik Катерина', 'katerina@keksik.com.ua'), ),
                       email.utils.formataddr(('Директор Интернет магазин Keksik Светлана Витальевна', 'lana24680@keksik.com.ua'), ), ],
            html_content='discrepancy_price: {0}<br />\n{1}'.format(discrepancy_price, discrepancy_price_html), )


def get_price(prices,  # type: list
              ):
    # type: (...) -> dict
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
