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
        try:
            logging_log_info.info('self = {0}'.format(self))
            logging_log_info.info('self.__class__ = {0}'.format(self.__class__))
            # logging_log_info.info('self.__doc__ = {0}'.format(self.__doc__))
            logging_log_info.info('self.__module__= {0}'.format(self.__module__))
            # logging_log_info.info('self.__repr__() = {0}'.format(self.__repr__()))
            # logging_log_info.info('object = {0}'.format(object))
            # logging_log_info.info('object.__class__ = {0}'.format(object.__class__))
            # logging_log_info.info('object.__doc__ = {0}'.format(object.__doc__))
            # logging_log_info.info('object.__module__ = {0}'.format(object.__module__))
            # logging_log_info.info('object.__repr__() = {0}'.format(object.__repr__()))
        except Exception as e:
            logging_log_error.error('Exception: {0}'.format(e))

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
