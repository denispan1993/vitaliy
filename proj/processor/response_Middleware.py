# -*- coding: utf-8 -*-
import time
from logging import getLogger

__author__ = 'AlexStarov'

logging = getLogger(__name__)

skip_url = ('/ajax/resolution/', '/ajax/cookie/', '/ajax/timezone/client/', '/ajax/geoip/resolve/', )


class Process_Response_Middleware(object):

    def process_response(self, request, response):
        full_path = request.path

        if full_path not in skip_url:
            logging.info(u'Stop executions (END): {0}'.format(time.time()))

        return response
