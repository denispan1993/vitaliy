# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from xml.dom.minidom import parse
import xml.etree.ElementTree as ET
from time import sleep
import os

__author__ = 'AlexStarov'


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

                #e = parse(file=path_and_filename, bufsize=1024)
                e = ET.parse(source=path_and_filename)
                root = e.getroot()
                #f = e.getElementsByTagName(u'Классификатор')[0]
                e = root.iter(u'Классификатор')
                for neihbor in e:
                    print neihbor, neihbor.tag, neihbor.attrib
#                print f.toxml()
#                print '#================='
#                print f.nodeName
#                print '#================='
#                print f.nodeValue
#                print '#================='
#                print f.nodeType, f.TEXT_NODE

