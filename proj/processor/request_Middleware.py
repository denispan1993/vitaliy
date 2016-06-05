# -*- coding: utf-8 -*-
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
                            return redirect(to=object, permanent=True)
                        except Exception as e:
                            logging.error(u'Error redirect to new_path: {0}'.format(e))

                    except Exception as e:
                        logging.error(u'Error: apps.slide.models.Slide: full_path = {0}'.format(e))

                elif not full_path.endswith('/'):
                    try:
                        view, args, kwargs = resolve(full_path + '/', )
                        logging.debug(u"resolve(full_path + '/', ): view = {0}, args = {1}, args = {2}".format(view, args, kwargs))
                        logging.error(u'Redirect to new_path: {0}'.format(full_path + '/'))

                        return redirect(to=full_path + '/', permanent=True)

                    except Exception as e:
                        logging.error(u"Error resolve(full_path + '/', ): full_path = {0}, Exception = {1}".format(full_path, e))

                else:
                    try:
                        value = full_path.split('/')[2].encode('cp1252')

                        if value[:2] == 'к':
                            model = Category
                        else:
                            model = Product

                        try:
                            object = model.objects.get(pk=value[6:])
                            logging.error(u'Object: {0}'.format(object))
                        except model.DoesNotExist:
                            pass

                        logging.error(u'Redirect to new_path: {0}'.format(object.get_absolute_url()))

                        try:
                            return redirect(to=object, permanent=True)
                        except Exception as e:
                            logging.error(u'Error redirect to new_path: {0}'.format(e))

                    except Exception as e:
                        logging.error(u'3Error: request.path = value Exception = {0}'.format(e))
