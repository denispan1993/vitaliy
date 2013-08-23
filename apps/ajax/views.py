# coding=utf-8
__author__ = 'user'

try:
    from django.utils.simplejson import dumps
    # import simplejson as json
except ImportError:
    from json import dumps
    # import json

from django.http import HttpResponse


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
            data = dumps(response, )
            mimetype = 'application/javascript'
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
            data = dumps(response, )
            mimetype = 'application/javascript'
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
            data = dumps(response, )
            mimetype = 'application/javascript'
            return HttpResponse(data, mimetype, )
        elif request.method == 'GET':
            return HttpResponse(status=400, )
        else:
            return HttpResponse(status=400, )
    else:
        return HttpResponse(status=400, )


def product_to_cart(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            request_cookie = request.session.get(u'cookie', None, )
            if request_cookie:
                product_pk = request.POST.get(u'product_pk', None, )
                if product_pk:
                    try:
                        product_pk = int(product_pk, )
                    except ValueError:
                        return HttpResponse(status=400, )
                    else:
                        from apps.product.views import add_to_cart
                        cart, product_in_cart = add_to_cart(request=request,
                                                            int_product_pk=product_pk, )
                        html = '<b>Позиций:</b> %s' \
                               '<br>' \
                               '<b>На сумму:</b> %s' \
                               ' грн. ' \
                               '%s' \
                               ' коп.<br>' % (cart.count_name_of_products,
                                              cart.summ_money_of_all_products_grn,
                                              cart.summ_money_of_all_products_kop, )
                        response = {'result': 'Ok',
                                    'html': html, }
                        data = dumps(response, )
                        mimetype = 'application/javascript'
                        return HttpResponse(data, mimetype, )
                else:
                    return HttpResponse(status=400, )
            else:
                return HttpResponse(status=400, )
        elif request.method == 'GET':
            return HttpResponse(status=400, )
        else:
            return HttpResponse(status=400, )
    else:
        return HttpResponse(status=400, )
