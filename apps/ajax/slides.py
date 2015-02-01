# coding=utf-8
__author__ = 'user'

try:
    from django.utils.simplejson import dumps
    # import simplejson as json
except ImportError:
    from json import dumps
    # import json

from django.http import HttpResponse


def left(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            request_cookie = request.session.get(u'cookie', None, )
            if request_cookie:
                main_left_Height = request.POST.get(u'main_left_Height', None, )
                main_center_Height = request.POST.get(u'main_center_Height', None, )
                lambda_Height = int(main_center_Height, ) - int(main_left_Height, )
                product_block_count = int(lambda_Height/300, )
                response = {'result': 'Ok',
                            'lambda_Height': lambda_Height,
                            'product_block_count': product_block_count,
                            'help_text': u'Номер купона не действительный', }
                data = dumps(response, )
                mimetype = 'application/javascript'
                return HttpResponse(data, mimetype, )
            else:
                return HttpResponse(status=400, )
        elif request.method == 'GET':
            return HttpResponse(status=400, )
        else:
            return HttpResponse(status=400, )
    else:
        return HttpResponse(status=400, )
