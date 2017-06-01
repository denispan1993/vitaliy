# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
import os

from applications.product.models import Category, Product, ItemID, Unit_of_Measurement

__author__ = 'AlexStarov'


def search_in_category(id_1c, name=None, parent=None, ):
    if not name:
        try:
            return Category.objects.get(id_1c=id_1c, )
        except Category.DoesNotExist:
            pass

    try:
        return Category.objects.get(title=name, id_1c=id_1c, parent=parent, )

    except Category.DoesNotExist:
        return Category.objects.create(
            title=name,
            id_1c=id_1c,
            parent=parent,
            url=name.replace(' ', '-').lower(),
            is_active=False)

    except Category.MultipleObjectsReturned:
        cats = Category.objects.filter(title=name, id_1c=id_1c, parent=parent, )
        if len(cats) > 1:
            raise 'MultiCat'
        elif len(cats) == 1:
            return cats[0]
        elif len(cats) == 0:
            try:
                return Category.objects.get(title=name, parent=parent)
            except Category.DoesNotExist:
                return Category.objects.create(
                    title=name,
                    id_1c=id_1c,
                    parent=parent,
                    url=name.replace(' ', '-').lower(),
                    is_active=False)


def get_products(products_list):
    success = 0
    unsuccess = 0
    unsuccess_itemid =''
    double = 0
    double_itemid = ''
    for product in products_list:
        product_list = list(product)
        itemid=product_list[1].text
        print(itemid, len(itemid))
        try:
            itemid = ItemID.objects.using('real').get(ItemID=product_list[1].text)
            success += 1
            print success, ': ', u'Артикул:-->"', product_list[1].text, '"<--:Found'
        except ItemID.DoesNotExist:
            unsuccess += 1
            double_itemid += '%s,' % product_list[1].text
            print unsuccess, ': ', u'Артикул:-->"', product_list[1].text, '"<--:Not Found'
        except ItemID.MultipleObjectsReturned:
            double += 1
            double_itemid += '%s,' % product_list[1].text
            print double, ': ', u'Артикул:-->"', product_list[1].text, '"<--:Not Found'

    print('success: ', success)
    print('unsuccess: ', unsuccess)
    print(unsuccess_itemid)
    print('double: ', double)
    print(double_itemid)


    #        try:
#            product = Product.objects.using('real').get(ItemID__ItemID=product_list[1].text)
#            success += 1
#            #product.id_1c = product_list[0].text
#            #product.save()
#            continue
#        except Product.DoesNotExist:
#            unsuccess += 1
#            print unsuccess, ': ', u'Артикул:-->', product_list[1].text, '<--:Not Found'

#    try:
#        products = Product.objects.using(alias='real').filter(id_1c__isnull=True, )
#        for product in products:
#            try:
#                print 'Product:->>', product.name, '<<-Not Found', u'Артикул:-->', product.ItemID.all()[0].ItemID
#            except IndexError:
#                print 'Product:->>', product.name, '<<-Not Found', u'Артикул:-->', 'AAAAAAAAAAAA!!!!!!!!!!!!!!!! CRASH!!!!!!!!!!!!!'
#    except Product.DoesNotExist:
#        pass

#        unit_of_measurement_pk = Unit_of_Measurement.objects.\
#            filter(name__icontains=product_list[3].text).\
#            values_list('pk', flat=True, )[0]

        # product = Product.objects.create(
#        product = Product(
#            id_1c=product_list[0].text,
#            is_active=False,
#            title=unicode(product_list[2].text),
#            name=product_list[2].text,
#            url=product_list[2].text.replace(' ', '-').lower(),
#            unit_of_measurement_id=unit_of_measurement_pk,
#            description=product_list[5].text,
#        )
#        print product_list[2].text

#        product.get_or_create_ItemID(itemid=product_list[1].tag)

#        for group in list(product_list[4]):
#            category = search_in_category(id_1c=group.text)
#            product.category.add(category)

    return None


def update_products(products_list):

    for product in products_list:
        product_list = list(product)

        try:
            real_product = Product.objects.get(id_1c=product_list[0].text)

            #real_product.
            print(u'Ид: ', product_list[0].text, ' real_product: ', real_product, ' quantity: ', product_list[5].text, )
        except Product.DoesNotExist:
            pass

    return None


def enter_the_level(level_list, level=1, parent=None):

    for elem_level_Indx, elem_level in enumerate(level_list):

        if level >= 2 and elem_level.tag == u'Ид' and level_list[elem_level_Indx + 1].tag == u'Наименование':

            parent = search_in_category(
                name=level_list[elem_level_Indx + 1].text,
                id_1c=elem_level.text,
                parent=parent, )

        if elem_level.tag == u'Наименование'\
            and elem_level.text == u'Классификатор (Каталог товаров)'\
            and level_list[elem_level_Indx+1].tag == u'Владелец'\
            and level_list[elem_level_Indx+2].tag == u'Группы':

            level += 1
            enter_the_level(level_list=list(level_list[elem_level_Indx+2]), level=level, )

        if elem_level.tag == u'Группа':

            enter_the_level(level_list=list(level_list[elem_level_Indx]), level=level, parent=parent)

        try:
            if elem_level.tag == u'Наименование'\
                    and level_list[elem_level_Indx + 1].tag == u'Группы':

                level += 1
                enter_the_level(list(level_list[elem_level_Indx + 1]), level=level, parent=parent)
        except IndexError:
            pass

        if elem_level.tag == u'Каталог товаров'\
                and level_list[elem_level_Indx+1].tag == u'Владелец'\
                and level_list[elem_level_Indx+2].tag == u'Товары':

            level += 1
            enter_the_level(level_list=list(level_list[elem_level_Indx+2]), level=level, )

    return None


class Command(BaseCommand, ):
    from optparse import make_option
    option_list = BaseCommand.option_list + (
        make_option('--id', '--pk', '--delivery_id', '--delivery_pk',
                    action='store', type='int', dest='delivery_pk',
                    help=''),
        make_option('--t', '--delivery_test', '--test',
                    action='store_true', dest='delivery_test',
                    help=''),
        make_option('--g', '--delivery_general', '--general',
                    action='store_true', dest='delivery_test',
                    help=''),
    )
    #self.verbosity = int(options.get('verbosity'))
    #def add_arguments(self, parser):
    #    parser.add_argument('delivery_id', nargs='+', type=int)

    def handle(self, *args, **options):
        cwd = os.getcwd()
        cwd = os.path.join(cwd, 'db')

        for name in os.listdir(cwd):
            path_and_filename = os.path.join(cwd, name)
            if os.path.isfile(path_and_filename, ) and name == 'import.xml':

                root = ET.parse(source=path_and_filename).getroot()
                for elem_first_level in root:

                    #if elem_first_level.tag == u'Классификатор':
                    #    enter_the_level(list(elem_first_level))

                    if elem_first_level.tag == u'Каталог':
                        elems_product_level = list(elem_first_level)

                        if elems_product_level[0].tag == u'Ид'\
                                and elems_product_level[1].tag == u'ИдКлассификатора'\
                                and elems_product_level[2].tag == u'Наименование'\
                                and elems_product_level[3].tag == u'Товары':

                            get_products(list(elems_product_level[3]))
