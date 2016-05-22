# -*- coding: utf-8 -*-
import time
from logging import getLogger

__author__ = 'AlexStarov'

debug_log = getLogger('log')


class Process_Response_Middleware(object):

    def process_response(self, request, response):
        print(u'Start executions (END): {0}'.format(time.time()))
        debug_log.info(u'Start executions (END): {0}'.format(time.time()))

        return response
