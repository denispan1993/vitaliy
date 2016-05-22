# -*- coding: utf-8 -*-
import time
from logging import getLogger

__author__ = 'AlexStarov'

debug_log = getLogger('log')


class Process_Request_Middleware(object):

    def process_request(self, request, ):
        print(u'Start executions (START): {0}'.format(time.time()))
        debug_log.info(u'Start executions (START): {0}'.format(time.time()))
