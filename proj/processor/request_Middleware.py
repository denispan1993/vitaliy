﻿# -*- coding: utf-8 -*-
import time
from django.core.urlresolvers import resolve, Resolver404
from django.shortcuts import redirect, HttpResponsePermanentRedirect
from logging import getLogger
from apps.product.models import Product, Category
from apps.product.views import show_product

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
                try:
                    logging.error(u'Error resolve(full_path, ): full_path = {0}, Exception = {1}'.format(full_path, e))
                except Exception as e:
                    logging.error(u'Error resolve(full_path, ): Exception = {0}'.format(e))

                if "{{ no such element: apps.slide.models.Slide object['url'] }}" in full_path:
                    try:
                        value = unicode(full_path.split('{{')[0])
                        view, args, kwargs = resolve(value, )
                        logging.debug(u"resolve(value, ) after split '{{': view = {0}, args = {1}, args = {2}".format(view, args, kwargs))

                        if view == show_product:
                            model = Product
                        else:
                            model = Category

                        try:
                            object = model.objects.get(pk=kwargs['id'])
                            logging.error(u'Object: {0}'.format(object))
                        except model.DoesNotExist:
                            pass

                        logging.error(u'Redirect to new_path: {0}'.format(object.get_absolute_url()))

                        try:
                            HttpResponsePermanentRedirect(object)
                        except Exception as e:
                            logging.error(u'Error redirect to new_path: {0}'.format(e))

                    except Exception as e:
                        logging.error(u'Error: apps.slide.models.Slide: full_path = {0}'.format(e))

                elif not full_path.endswith('/'):
                    try:
                        view, args, kwargs = resolve(full_path + '/', )
                        logging.debug(u"resolve(full_path + '/', ): view = {0}, args = {1}, args = {2}".format(view, args, kwargs))
                        logging.error(u'Redirect to new_path: {0}'.format(full_path + '/'))

                        HttpResponsePermanentRedirect(full_path + '/')

                    except Exception as e:
                        logging.error(u"Error resolve(full_path + '/', ): full_path = {0}, Exception = {1}".format(full_path, e))

                else:
                    try:
                        values = full_path.split('/')
                        for value in values:
                            logging.error(u"full_path.split('/') = {0}".format(value))

                        value = values[2]
                        logging.error(u'00Error: {0}'.format(value))
                        value = value.encode('cp1252')
                        logging.error(u'01Error: {0}'.format(value))
                        try:
                            logging.error(u'full_path.decode("cp1252").encode("utf8") = {0}'.format(value))
                            try:
                                HttpResponsePermanentRedirect(value)
                            except Exception as e:
                                logging.error(u'1Error: request.path = value Exception = {0}'.format(e))
                        except Exception as e:
                            logging.error(u'2Error: request.path = value Exception = {0}'.format(e))
                    except Exception as e:
                        logging.error(u'3Error: request.path = value Exception = {0}'.format(e))

                    try:
                        value = full_path.encode('cp1252')
                        try:
                            logging.error(u'full_path.decode("cp1252") = {0}'.format(value))
                            try:
                                request.path = value
                            except Exception as e:
                                logging.error(u'Error: request.path = value Exception = {0}'.format(e))
                        except Exception as e:
                            logging.error(u'Error: request.path = value Exception = {0}'.format(e))
                    except Exception as e:
                        logging.error(u'Error: request.path = value Exception = {0}'.format(e))
