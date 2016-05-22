# -*- coding: utf-8 -*-
import time
from logging import getLogger

__author__ = 'AlexStarov'

logging = getLogger(__name__)


class Process_Response_Middleware(object):

    def process_response(self, request, response):
        logging.info(u'Stop executions (END): {0}'.format(time.time()))

        return response
