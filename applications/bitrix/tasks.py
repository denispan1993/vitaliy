# -*- coding: utf-8 -*-
import os
import time
from datetime import datetime, date
import xml.etree.ElementTree as ET
from celery.utils.log import get_task_logger
from proj.celery import celery_app

from proj import settings
from .import_utils_process_import_xml import process_import_xml
from .import_utils_process_offers_xml import process_offers_xml

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)


@celery_app.task()
def process_bitrix_import_xml(*args, **kwargs):

    start = time.time()

    path_and_filename = kwargs.get('path_and_filename', False)

    print('os.path.isfile(path_and_filename, )', os.path.isfile(path_and_filename, ), path_and_filename,
          path_and_filename.split('.')[0], type(path_and_filename.split('.')[0]),
          path_and_filename.split('.')[0].split('/')[-1], type(path_and_filename.split('.')[0].split('/')[-1]),
          path_and_filename.split('.')[1], int(path_and_filename.split('.')[1]), type(path_and_filename.split('.')[1]),
          path_and_filename.split('.')[2], int(path_and_filename.split('.')[2]), type(path_and_filename.split('.')[2]),
          path_and_filename.split('.')[-1], type(path_and_filename.split('.')[-1]), )

    if os.path.isfile(path_and_filename, )\
            and path_and_filename.split('.')[0].split('/')[-1] == 'import'\
            and path_and_filename.split('.')[-1] == 'xml':

        print('os.path.isfile(path_and_filename, )', os.path.isfile(path_and_filename, ), path_and_filename,
              path_and_filename.split('.')[1], type(path_and_filename.split('.')[1]),
              path_and_filename.split('.')[2], type(path_and_filename.split('.')[2]), )

        for elem_first_level in ET.parse(source=path_and_filename, ).getroot():

            if elem_first_level.tag == u'Каталог':

                elems_product_level = list(elem_first_level, )

                if elems_product_level[0].tag == u'Ид' \
                        and elems_product_level[1].tag == u'ИдКлассификатора' \
                        and elems_product_level[2].tag == u'Наименование' \
                        and elems_product_level[3].tag == u'Владелец'\
                        and elems_product_level[4].tag == u'Товары':

                    process_import_xml(list(elems_product_level[4], ), )

    logger.info('Process time: {}'.format(time.time() - start, ), )

    return True, datetime.now(), '__name__: {0}'.format(str(__name__, ), )


@celery_app.task()
def process_bitrix_offers_xml(*args, **kwargs):

    start = time.time()

    path_and_filename = kwargs.get('path_and_filename', False)

    if os.path.isfile(path_and_filename, )\
            and path_and_filename.split('.')[0].split('/')[-1] == 'offers'\
            and path_and_filename.split('.')[-1] == 'xml':

        print('os.path.isfile(path_and_filename, )', os.path.isfile(path_and_filename, ),
              path_and_filename.split('.')[1], type(path_and_filename.split('.')[1]),
              path_and_filename.split('.')[2], type(path_and_filename.split('.')[2]), )

        for elem_second_level in list(ET.parse(source=path_and_filename, ).getroot()[0]):

            if elem_second_level.tag == u'Предложения':

                process_offers_xml(offers_list=list(elem_second_level, ), )

    logger.info('Process time: {}'.format(time.time() - start, ), )

    return True, datetime.now(), '__name__: {0}'.format(str(__name__, ), )
