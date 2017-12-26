# -*- coding: utf-8 -*-
import os
import time
from datetime import datetime, date
import xml.etree.ElementTree as ET
from celery.utils.log import get_task_logger
from proj.celery import celery_app

from .utils import get_products, process_of_proposal

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

    logger.info('Process time: {}'.format(time.time() - start, ), )

    return True, datetime.now(), '__name__: {0}'.format(str(__name__, ), )
