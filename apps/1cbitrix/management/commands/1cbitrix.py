# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
from time import sleep
import os

from apps.product.models import Category

__author__ = 'AlexStarov'


def search_in_category(name, id_1c, parent=None, ):
    try:
        if parent:
            return Category.objects.get(title__icontains=name, parent=parent)
        else:
            return Category.objects.get(title__icontains=name)
    except Category.DoesNotExist:
        cat = Category()
        cat.title = name
        if parent:
            cat.parent = parent
        cat.id_1c = id_1c
        cat.save()
        return cat
    except Category.MultipleObjectsReturned:
        if parent:
            cats = Category.objects.filter(title=name, parent=parent)
            if len(cats) > 1:
                raise 'MultiCat'
            elif len(cats) == 1:
                return cats[0]
            elif len(cats) == 0:
                try:
                    cat = Category.objects.get(title=name, parent=parent)
                except Category.DoesNotExist:
                    cat = Category()
                    cat.title = name
                    if parent:
                        cat.parent = parent
                    cat.id_1c = id_1c
                    cat.save()
                    return cat


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
                for elem_level1 in root:
                    # print 'level1', elem_level1, elem_level1.tag, elem_level1.attrib, elem_level1.text

                    if elem_level1.tag == u'Классификатор':

                        elems_level1 = list(elem_level1)

                        for elem_level2_Indx, elem_level2 in enumerate(elems_level1):
                            # print 'level2', elem_level2_Indx, elem_level2, elem_level2.tag, elem_level2.attrib, elem_level2.text

                            if elem_level2.tag == u'Наименование'\
                                    and elem_level2.text == u'Классификатор (Каталог товаров)'\
                                    and elems_level1[elem_level2_Indx+1].tag == u'Группы':

                                elems_level2 = list(elems_level1[elem_level2_Indx+1])

                                for elem_level3_Indx, elem_level3 in enumerate(elems_level2):
                                    # print 'level3', elem_level3_Indx, elem_level3, elem_level3.tag, elem_level3.attrib, elem_level3.text

                                    elems_level3 = list(elem_level3)

                                    for elem_level4_Indx, elem_level4 in enumerate(elems_level3):
                                        # print 'level4', elem_level4_Indx, elem_level4, elem_level4.tag, elem_level4.attrib, elem_level4.text

                                        if elem_level4.tag == u'Наименование' \
                                                and elem_level4.text == u'Товары' \
                                                and elems_level3[elem_level4_Indx + 1].tag == u'Группы':

                                            elems_level4 = list(elems_level3[elem_level4_Indx + 1])

                                            for elem_level5_Indx, elem_level5 in enumerate(elems_level4):
                                                # print 'level5', elem_level5_Indx, elem_level5, elem_level5.tag, elem_level5.attrib, elem_level5.text

                                                if elem_level5.tag == u'Группа':

                                                    try:
                                                        elems_level5 = list(elems_level4[elem_level5_Indx])

                                                        for elem_level6_Indx, elem_level6 in enumerate(elems_level5):
                                                            # print 'level6', elem_level6_Indx, elem_level6, elem_level6.tag, elem_level6.attrib, elem_level6.text

                                                            if elem_level6.tag == u'Ид' and elems_level5[elem_level6_Indx + 1].tag == u'Наименование':
                                                                dict_elem_level6 = {'Id': elem_level6.text, 'Name': elems_level5[elem_level6_Indx + 1].text, }

                                                                parent_cat6 = search_in_category(name=dict_elem_level6['Name'], id_1c=dict_elem_level6['Id'])
                                                                print 'level6: ', dict_elem_level6, parent_cat6

                                                            if elem_level6.tag == u'Группы':
                                                                elems_level6 = list(elems_level5[elem_level6_Indx])

                                                                for elem_level7_Indx, elem_level7 in enumerate(elems_level6):
                                                                    # print 'level7', elem_level7_Indx, elem_level7, elem_level7.tag, elem_level7.attrib, elem_level7.text
                                                                    if elem_level7.tag == u'Группа':
                                                                        try:
                                                                            elems_level7 = list(elems_level6[elem_level7_Indx])

                                                                            for elem_level8_Indx, elem_level8 in enumerate(elems_level7):
                                                                                # print 'level8', elem_level8_Indx, elem_level8, elem_level8.tag, elem_level8.attrib, elem_level8.text

                                                                                if elem_level8.tag == u'Ид' and elems_level7[elem_level8_Indx + 1].tag == u'Наименование':
                                                                                    dict_elem_level8 = {'Id': elem_level8.text, 'Name': elems_level7[elem_level8_Indx + 1].text, }

                                                                                    parent_cat8 = search_in_category(name=dict_elem_level8['Name'], id_1c=dict_elem_level8['Id'], parent=parent_cat6)
                                                                                    print 'level6: ', dict_elem_level6, parent_cat8

                                                                                if elem_level8.tag == u'Группы':
                                                                                    elems_level8 = list(elems_level7[elem_level8_Indx])

                                                                                    for elem_level9_Indx, elem_level9 in enumerate(elems_level8):
                                                                                        # print 'level9', elem_level9_Indx, elem_level9, elem_level9.tag, elem_level9.attrib, elem_level9.text
                                                                                        if elem_level9.tag == u'Группа':
                                                                                            try:
                                                                                                elems_level9 = list(elems_level8[elem_level9_Indx])

                                                                                                for elem_level10_Indx, elem_level10 in enumerate(elems_level9):
                                                                                                    # print 'level10', elem_level10_Indx, elem_level10, elem_level10.tag, elem_level8.attrib, elem_level10.text

                                                                                                    if elem_level10.tag == u'Ид' and elems_level9[elem_level10_Indx + 1].tag == u'Наименование':
                                                                                                        dict_elem_level10 = {'Id': elem_level10.text, 'Name': elems_level9[elem_level10_Indx + 1].text, }

                                                                                                        parent_cat10 = search_in_category(name=dict_elem_level10['Name'], id_1c=dict_elem_level10['Id'], parent=parent_cat8)
                                                                                                        print 'level6: ', dict_elem_level6, parent_cat10

                                                                                                    if elem_level10.tag == u'Группы':
                                                                                                        level10 = True
                                                                                            except IndexError:
                                                                                                pass

                                                                        except IndexError:
                                                                            pass

                                                    except IndexError:
                                                        pass

        if 'level10' in locals():
            print 'level10'
