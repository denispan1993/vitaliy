# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'


try:
    from django.utils.simplejson import dumps
    # import simplejson as json
except ImportError:
    from json import dumps
    # import json

from django.http import HttpResponse


def client_timezone(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            response = {'result': 'Ok', }
            # request.session[u'ajax_timezone'] = True
            ajax_timezone_offset = request.session.get(u'ajax_timezone_offset', False, )
            request.session[u'ajax_timezone_offset'] = ajax_timezone_offset
            from datetime import datetime
            request.session[u'ajax_timezone_datetime'] = str(datetime.now(), )
            # response = {'result': 'Please enable cookies and try again.', }
            # request.session[u'cookie'] = False
            data = dumps(response, )
            mimetype = 'application/javascript'
            return HttpResponse(data, mimetype, )
        elif request.method == 'GET':
            return HttpResponse(status=400, )
        else:
            return HttpResponse(status=400, )
    else:
        return HttpResponse(status=400, )
