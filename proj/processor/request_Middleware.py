# -*- coding: utf-8 -*-
import time
from django.core.urlresolvers import resolve, Resolver404
from logging import getLogger

__author__ = 'AlexStarov'

logging_log_info = getLogger('log_info')
logging_log_debug = getLogger('log_debug')
logging_log_error = getLogger('log_error')


class Process_Request_Middleware(object):

    def process_request(self, request, ):
        logging_log_info.info(u'')
        logging_log_info.info(u'Start executions (START): {0}'.format(time.time()))

        logging_log_info.info(u'resolve: Process_Request_Middleware')

        full_path = request.path
        logging_log_debug.debug(u'full_path: {0}'.format(full_path))

        try:
            view, args, kwargs = resolve(full_path, )
            logging_log_debug.debug(u'resolve(full_path, ): view = {0}, args = {1}, args = {2}'.format(view, args, kwargs))
        except Exception as e:
            logging_log_error.error(u'Error resolve(full_path, ): full_path = {0}'.format(full_path))

            try:
                value = full_path.decode('cp1252').encode('utf8')
            except:
                pass
            else:
                try:
                    logging_log_error.error("full_path.decode('cp1252').encode('utf8') = {0}".format(value))
                except:
                    pass
            try:
                value = full_path.encode('cp1252')
            except:
                pass
            else:
                try:
                    logging_log_error.error("full_path.decode('cp1252') = {0}".format(value))
                except:
                    pass
