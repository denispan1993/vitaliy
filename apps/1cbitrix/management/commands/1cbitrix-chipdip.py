# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
from time import sleep
from urllib import unquote
import os

from apps.product.models import Category, Product

__author__ = 'AlexStarov'


def search_in_category(name, id_1c, parent=None, ):
    try:
        return Category.objects.get(title=name, id_1c=id_1c, parent=parent, )

    except Category.DoesNotExist:
        print name
        return Category.objects.create(title=name, id_1c=id_1c, parent=parent, url=name.replace(' ', '-'), is_active=False)

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
                return Category.objects.create(title=name, id_1c=id_1c, parent=parent, url=name.replace(' ', '-'), is_active=False)


def add_product(product_list):

    product = Product()
    product.id_1c = product_list[0].tag

    product.get_or_create_ItemID(itemid=product_list[1].tag)

    product.title = product_list[2].tag
    product.name = product_list[2].tag

        and level_list[elem_level_Indx+3].tag == u'БазоваяЕдиница'\
        and level_list[elem_level_Indx+4].tag == u'Группы':

    return None


def enter_the_level(level_list, level=1, parent=None):

    for elem_level_Indx, elem_level in enumerate(level_list):

        if level >= 2 and elem_level.tag == u'Ид' and level_list[elem_level_Indx + 1].tag == u'Наименование':

            parent = search_in_category(name=level_list[elem_level_Indx + 1].text, id_1c=elem_level.text, parent=parent, )

        print level, elem_level_Indx, elem_level, elem_level.tag, elem_level.attrib, elem_level.text

        if elem_level.tag == u'Наименование'\
            and elem_level.text == u'Классификатор (Каталог товаров)'\
            and level_list[elem_level_Indx+1].tag == u'Владелец'\
            and level_list[elem_level_Indx+2].tag == u'Группы':

            level += 1
            enter_the_level(level_list=list(level_list[elem_level_Indx+2]), level=level, )

        if elem_level.tag == u'Группа'\
            or elem_level.tag == u'Товар':

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

        try:
            if elem_level.tag == u'Ид'\
                and level_list[elem_level_Indx+1].tag == u'Артикул'\
                and level_list[elem_level_Indx+2].tag == u'Наименование'\
                and level_list[elem_level_Indx+3].tag == u'БазоваяЕдиница'\
                and level_list[elem_level_Indx+4].tag == u'Группы':
                """ То это точно товар """
                add_product(level_list)

        except IndexError:
            pass

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
        cwd = os.path.join(cwd, 'db\chipdip')

        for name in os.listdir(cwd):
            path_and_filename = os.path.join(cwd, name)
            if os.path.isfile(path_and_filename, ) and name == 'import.xml':

                root = ET.parse(source=path_and_filename).getroot()
                for elem_level1 in root:

                    if elem_level1.tag == u'Классификатор':
                        enter_the_level(list(elem_level1))


                    if elem_level1.tag == u'Каталог товаров':
                        elems_level1 = list(elem_level1)

                        for elem_level2_Indx, elem_level2 in enumerate(elems_level1):

                            if elem_level2.tag == u'Наименование' \
                                    and elem_level2.text == u'Каталог товаров' \
                                    and elems_level1[elem_level2_Indx + 1].tag == u'Товары':

                                elems_level2 = list(elems_level1[elem_level2_Indx + 1])

                                for elem_level3_Indx, elem_level3 in enumerate(elems_level2):
                                    # print 'level3', elem_level3_Indx, elem_level3, elem_level3.tag, elem_level3.attrib, elem_level3.text

                                    if elem_level3.tag == u'Товар':

                                        elems_level3 = list(elem_level3)

                                        for elem_level4_Indx, elem_level4 in enumerate(elems_level3):
                                            # print 'level4', elem_level4_Indx, elem_level4, elem_level4.tag, elem_level4.attrib, elem_level4.text

                                            if elem_level4.tag == u'Ид':
                                                id_1c_prod = elem_level4.text
                                            if elems_level3[elem_level4_Indx + 1].tag == u'Артикул':
                                                articul = elems_level3[elem_level4_Indx + 1].text
                                            if elems_level3[elem_level4_Indx + 2].tag == u'Наименование':
                                                name = elems_level3[elem_level4_Indx + 2].text

                                            if elem_level4.tag == u'Группы':

                                                elems_level4 = list(elems_level3[elem_level4_Indx])

                                                for elem_level5_Indx, elem_level5 in enumerate(elems_level4):
                                                    # print 'level5', elem_level5_Indx, elem_level5, elem_level5.tag, elem_level5.attrib, elem_level5.text

                                                    if elem_level5.tag == u'Ид':
                                                        id_1c_cat = elem_level5.text

        if 'level10' in locals():
            print 'level10'
