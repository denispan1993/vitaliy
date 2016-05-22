# -*- coding: utf-8 -*-
import time
from django.core.urlresolvers import resolve, Resolver404
from logging import getLogger

__author__ = 'AlexStarov'

logging = getLogger(__name__)

skip_url = ('/ajax/resolution/', '/ajax/cookie/', '/ajax/timezone/client/', '/ajax/geoip/resolve/', )


class Process_Request_Middleware(object):

    def process_request(self, request, ):
        full_path = request.path

        if full_path not in skip_url:

            logging.info(u'')

            logging.info(u'Start executions (START): {0}'.format(time.time()))

            logging.info(u'resolve: Process_Request_Middleware')

            logging.debug(u'full_path: {0}'.format(full_path))

            try:
                view, args, kwargs = resolve(full_path, )
                logging.debug(u'resolve(full_path, ): view = {0}, args = {1}, args = {2}'.format(view, args, kwargs))
            except Exception as e:
                logging.error(u'Error resolve(full_path, ): full_path = {0}'.format(full_path))

                try:
                    value = full_path.decode('cp1252').encode('utf8')
                except:
                    pass
                else:
                    try:
                        logging.error(u"full_path.decode('cp1252').encode('utf8') = {0}".format(value))
                    except:
                        pass
                try:
                    value = full_path.encode('cp1252')
                except:
                    pass
                else:
                    try:
                        logging.error(u"full_path.decode('cp1252') = {0}".format(value))
                        request.path = value
                    except:
                        pass
