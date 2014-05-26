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
            import django
            django_version = django.VERSION
            from datetime import datetime
            if int(django_version[0], ) == 1 and int(django_version[1], ) >= 6:
                request.session[u'ajax_resolution_datetime'] = str(datetime.now(), )
            elif int(django_version[0], ) == 1 and int(django_version[1], ) == 5:
                request.session[u'ajax_resolution_datetime'] = datetime.now()

            json_response = dumps(response, )
            # mimetype = 'application/json'
            return HttpResponse(content=json_response, content_type='application/javascript', )
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
                           '<input type="number" name="warehouse_number" id="warehouse_number"/>'
                    response = {'result': 'Ok',
                                'sel_country': 1,
                                'html': html, }
                else:
                    html = '<br />' \
                           '<label for="address">Полный адрес</label>' \
                           '<textarea cols="50" rows="5" name="address" id="address"></textarea>' \
                           '<br />' \
                           '<label for="postcode">Почтовый индекс</label>' \
                           '<input type="number" name="postcode" id="postcode"/>'
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
                available_to_order = request.POST.get(u'available_to_order', False, )
                if product_pk:
                    try:
                        product_pk = int(product_pk, )
                    except ValueError:
                        return HttpResponse(status=400, )
                    else:
                        from apps.product.views import add_to_cart
                        # print product_pk
                        cart, product_in_cart = add_to_cart(request=request,
                                                            int_product_pk=product_pk,
                                                            available_to_order=available_to_order, )
                        # print cart
                        # print product_in_cart
                        html = '<b>Позиций:</b> %s' \
                               '<br>' \
                               '<b>На сумму:</b> %s грн. ' \
                               '%s ' \
                               'коп.<br>' % (cart.count_name_of_products,
                                             cart.summ_money_of_all_products_integral(request, ),
                                             cart.summ_money_of_all_products_fractional(request, ), )
                        response = {'product_pk': product_pk,
                                    'result': 'Ok',
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


def order_change(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            request_cookie = request.session.get(u'cookie', None, )
            if request_cookie:
                action = request.POST.get(u'action', None, )
                if action == 'change_in_the_quantity':
                    """ Изменение количества единиц конкретного товара
                    """
                    product_pk = request.POST.get(u'product_pk', None, )
                    if product_pk:
                        try:
                            product_pk = int(product_pk, )
                        except ValueError:
                            return HttpResponse(status=400, )
                        else:
                            from apps.cart.models import Product
                            product = Product.objects.get(pk=product_pk, )
                            quantity = request.POST.get(u'quantity', None, )
                            try:
                                quantity = int(quantity, )
                            except ValueError:
                                return HttpResponse(status=400, )
                            else:
                                product.update_quantity(quantity=quantity, )
                                price = product.update_price_per_piece()
                                response = {'product_pk': product_pk,
                                            'product_price': float(price, ),
                                            'result': 'Ok', }
                                data = dumps(response, )
                                mimetype = 'application/javascript'
                                return HttpResponse(data, mimetype, )
                    else:
                        return HttpResponse(status=400, )
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
