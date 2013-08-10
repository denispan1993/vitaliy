# coding=utf-8
__author__ = 'user'


def resolution(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            width = request.POST.get(u'width', None, )
            if width:
                try:
                    width = int(width, )
                except ValueError:
                    response = {'result': 'Bad', }
                    request.session[u'width'] = 1024
                else:
                    response = {'result': 'Ok', }
                    request.session[u'width'] = width
            else:
                response = {'result': 'Bad', }
                request.session[u'width'] = 1024
            from datetime import datetime
            request.session[u'ajax_resolution_datetime'] = datetime.now()
# 1
#            import json
#            data = json.dumps(response, )
# 2
#            format = 'json'
#            from django.core import serializers
#            data = serializers.serialize(format, response, )
# 3
#            from django.utils import simplejson
#            data = simplejson.dumps({'a': 1})
            from django.utils.simplejson import dumps
            data = dumps(response, )
            mimetype = 'application/javascript'
            from django.http import HttpResponse
            return HttpResponse(data, mimetype, )
        elif request.method == 'GET':
            return HttpResponse(status=400, )
        else:
            return HttpResponse(status=400, )
    else:
        return HttpResponse(status=400, )


def cookie(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            if request.session.test_cookie_worked():
                response = {'result': 'Ok', }
                request.session[u'cookie'] = True
#                request.session.delete_test_cookie()
            else:
                response = {'result': 'Please enable cookies and try again.', }
                request.session[u'cookie'] = False
#                request.session.delete_test_cookie()
            from django.utils.simplejson import dumps
            data = dumps(response, )
            mimetype = 'application/javascript'
            from django.http import HttpResponse
            return HttpResponse(data, mimetype, )
        elif request.method == 'GET':
            return HttpResponse(status=400, )
        else:
            return HttpResponse(status=400, )
    else:
        return HttpResponse(status=400, )


def sel_country(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            request_cookie = request.session.get(u'cookie', None, )
            if request_cookie:
                country_pk = request.POST.get(u'country_pk', None, )
                if country_pk == '1':
                    html = '<br />' \
                           '<label for="region">Область</label>' \
                           '<input type="text" name="region" id="region"/>' \
                           '<br />' \
                           '<label for="settlement">Город (населённый пункт)</label>' \
                           '<input type="text" name="settlement" id="settlement"/>' \
                           '<br />' \
                           '<label for="warehouse_number">Номер склада "Новой почты"</label>' \
                           '<input type="text" name="warehouse_number" id="warehouse_number"/>'
                    response = {'result': 'Ok',
                                'sel_country': 1,
                                'html': html, }
                else:
                    html = '<br />' \
                           '<label for="address">Полный адрес</label>' \
                           '<textarea cols="50" rows="5" name="address" id="address"></textarea>' \
                           '<br />' \
                           '<label for="postcode">Почтовый индекс</label>' \
                           '<input type="text" name="postcode" id="postcode"/>'
                    response = {'result': 'Ok',
                                'sel_country': 2,
                                'html': html, }
            try:
                from django.utils.simplejson import dumps
                # import simplejson as json
            except ImportError:
                from json import dumps
                # import json
            data = dumps(response, )
            mimetype = 'application/javascript'
            from django.http import HttpResponse
            return HttpResponse(data, mimetype, )
        elif request.method == 'GET':
            return HttpResponse(status=400, )
        else:
            return HttpResponse(status=400, )
    else:
        return HttpResponse(status=400, )
