# -*- coding: utf-8 -*-
__author__ = 'Alex Starov'

try:
    from django.utils.simplejson import dumps
    # import simplejson as json
except ImportError:
    from json import dumps
    # import json

from django.http import HttpResponse


def callback_data_send(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            request_cookie = request.session.get(u'cookie', None, )
            if request_cookie:
                sessionid = request.POST.get(u'sessionid', None, )
                userid = request.POST.get(u'userid', None, )
                name = request.POST.get(u'name', None, )
                email = request.POST.get(u'email', None, )
                emailok = request.POST.get(u'emailok', None, )
                phone = request.POST.get(u'phone', None, )
                from apps.callback.models import CallBack
                try:
                    CallBack.objects.create(sessionid=sessionid,
                                            userid=userid,
                                            name=name,
                                            email=email,
                                            emailok=emailok,
                                            phone=phone, )
                except Exception as e:
                    print e.message
                    response = {'result': 'Bad',
                                'error': e.message, }
                    data = dumps(response, )
                    mimetype = 'application/javascript'
                    return HttpResponse(data, mimetype, )
                else:
                    response = {'result': 'Ok', }
                    data = dumps(response, )
                    mimetype = 'application/javascript'
                    return HttpResponse(data, mimetype, )
            else:
                response = {'result': 'Bad',
                            'error': u'Вы только-что зашли на сайт!!!', }
                data = dumps(response, )
                mimetype = 'application/javascript'
                return HttpResponse(data, mimetype, )
        elif request.method == 'GET':
            return HttpResponse(status=400, )
        else:
            return HttpResponse(status=400, )
    else:
        return HttpResponse(status=400, )
