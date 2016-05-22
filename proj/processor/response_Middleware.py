# -*- coding: utf-8 -*-
import time
from logging import getLogger

__author__ = 'AlexStarov'

logging_log_info = getLogger('log_info')


class Process_Response_Middleware(object):

    def process_response(self, request, response):
        logging_log_info.info(u'Stop executions (END): {0}'.format(time.time()))

        return response
