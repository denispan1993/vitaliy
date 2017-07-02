# -*- coding: utf-8 -*-
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from proj.celery import celery_app
from logging import getLogger
from celery.utils.log import get_task_logger
from urllib.parse import urlencode

from .models import Product

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)
std_logger = getLogger(__name__)


def decorate(func):
    # start = time.time()
    # print(u'Декорируем %s(*args, **kwargs): | Start: %s' % (func.__name__, start, ), )
    # logger.info(u'Декорируем %s... | Start: %s' % (func.__name__, start, ), )

    def wrapped(*args, **kwargs):
        start = time.time()
        print(u'Декорируем %s(*args, **kwargs): | Start: %s' % (func.__name__, start,), )
        logger.info(u'Декорируем %s... | Start: %s' % (func.__name__, start,), )

        print(u'Вызываем обёрнутую функцию с аргументами: *args и **kwargs ', )
        logger.info(u'Вызываем обёрнутую функцию с аргументами: *args и **kwargs ', )
        result = func(*args, **kwargs)

        stop = time.time()
        print(u'выполнено! | Stop: %s | Running time: %s' % (stop, stop - start,), )
        logger.info(u'выполнено! | Stop: %s | Running time: %s' % (stop, stop - start,), )

        return result

    # stop = time.time()
    # print(u'выполнено! | Stop: %s | Running time: %s' % (stop, stop - start, ), )
    # logger.info(u'выполнено! | Stop: %s | Running time: %s' % (stop, stop - start, ), )

    return wrapped

user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/48.0.2564.116 ' \
             'Safari/537.36'
headers = {'User-Agent': user_agent, }


@celery_app.task(name='product.tasks.check_page_in_index', )
def check_page_in_index(*args, **kwargs):

    start = datetime.now()
    logger.info(u'Start: processing_action(*args, **kwargs)', )
    logger.info(u'logger = get_task_logger(__name__): message: datetime.now() {0}'.format(start), )
    std_logger.info(u'std_logger = getLogger(__name__): message: datetime.now() {0}'.format(start), )

    try:
        product = Product.objects.published().order_by('check_page_in_index').first()
        url = product.get_absolute_url()
        logger.info(url)
    except Product.DoesNotExist:
        return False, datetime.now(), '__name__: {0}'.format(str(__name__, ), )

    """ Google """
    google = 'https://www.google.com/search?'\
             + urlencode({'q': 'info:{url}'.format(url=url, ), }, )
    data = requests.get(google, headers=headers, )
    data.encoding = 'ISO-8859-1'
    soup = BeautifulSoup(str(data.content), 'html.parser')
    try:
        check = soup.find(id="rso").find("div").find("div").find("h3").find("a")
        logger.info(" is indexed!")
    except AttributeError:
        logger.info(" is NOT indexed!")

    stop = datetime.now()
    logger.info(u'message: datetime.now() {0}'.format(stop, ), )
    logger.info(u'Stop: processing_action(*args, **kwargs): %s' % (stop - start), )

    return True, datetime.now(), '__name__: {0}'.format(str(__name__, ), )