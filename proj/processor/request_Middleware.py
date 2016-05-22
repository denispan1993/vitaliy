# -*- coding: utf-8 -*-
import time
from django.core.urlresolvers import resolve, Resolver404
from logging import getLogger

__author__ = 'AlexStarov'

debug_log = getLogger('log')


class Process_Request_Middleware(object):

    def process_request(self, request, ):
        debug_log.info(u'')
        debug_log.info(u'Start executions (START): {0}'.format(time.time()))

        debug_log.info(u'resolve: Process_Request_Middleware')

        full_path = request.path
        debug_log.debug(u'full_path: {0}'.format(full_path))

        try:
            view, args, kwargs = resolve(full_path, )
            debug_log.debug(u'resolve(full_path, ): view = {0}, args = {1}, args = {2}'.format(view, args, kwargs))
        except Exception as e:
            debug_log.error(u'Error resolve(full_path, ): full_path = {0}'.format(full_path))
