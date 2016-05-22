# -*- coding: utf-8 -*-
import time
from django.core.urlresolvers import resolve, Resolver404
from logging import getLogger

__author__ = 'AlexStarov'

debug_log = getLogger('log')


class Process_Request_Middleware(object):

    def process_request(self, request, ):
        print(u'Start executions (START): {0}'.format(time.time()))
        full_path = request.path
        view, args, kwargs = resolve(full_path, )
        print 'resolve: Process_Request_Middleware'
        print 'resolve(full_path, ) : view = ', view, ' args = ', args, ' kwargs = ', kwargs

        debug_log.info(u'Start executions (START): {0}'.format(time.time()))
