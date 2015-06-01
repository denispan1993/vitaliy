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
                from django.template.loader import render_to_string

                if country_pk == '1':
                    template_name = u'apps/ajax/templates/templatetags/block_show_order_ukraine.jinja2.html'
                    from apps.cart.models import DeliveryCompany
                    try:
                        delivery_companies_list = DeliveryCompany.objects.all()
                    except DeliveryCompany.DoesNotExist:
                        delivery_companies_list = None

                    html = render_to_string(template_name,
                                            dictionary={'request': request,
                                                        'delivery_companies_list': delivery_companies_list, }, )
                    # html = '<br />' \
                    #        '<label for="region">Область</label>' \
                    #        '<input type="text" name="region" id="region"/>' \
                    #        '<br />' \
                    #        '<label for="settlement">Город (населённый пункт)</label>' \
                    #        '<input type="text" name="settlement" id="settlement"/>' \
                    #        '<br />' \
                    #        '<label for="warehouse_number">Номер склада "Новой почты"</label>' \
                    #        '<input type="number" name="warehouse_number" id="warehouse_number"/>'
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
            """ Да мне должно быть пофиг на этом этапе,
            обрабатывает клиент cookies или нет """
            # request_cookie = request.session.get(u'cookie', None, )
            # if request_cookie:
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
                                         cart.sum_money_of_all_products_integral(request, ),
                                         cart.sum_money_of_all_products_fractional(request, ), )
                    response = {'product_pk': product_pk,
                                'result': 'Ok',
                                'html': html, }
                    data = dumps(response, )
                    mimetype = 'application/javascript'
                    return HttpResponse(data, mimetype, )
            else:
                return HttpResponse(status=400, )
            # else:
            #     return HttpResponse(status=400, )
        elif request.method == 'GET':
            return HttpResponse(status=400, )
        else:
            return HttpResponse(status=400, )
    else:
        return HttpResponse(status=400, )




def order_change(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            # request_cookie = request.session.get(u'cookie', None, )
            # if request_cookie:
                product_pk = request.POST.get(u'product_pk', None, )
                try:
                    product_pk = int(product_pk, )
                except ValueError:
                    print '9'
                    return HttpResponse(status=400, )
                else:
                    action = request.POST.get(u'action', None, )
                    if action == 'change_in_the_quantity'\
                            or action == 'change_delete':
                        from apps.cart.models import Product
                        product = Product.objects.get(pk=product_pk, )
                        quantity = 0
                        if action is 'change_in_the_quantity':
                            quantity = request.POST.get(u'quantity', None, )
                        try:
                            quantity = int(quantity, )
                        except ValueError:
                            return HttpResponse(status=400, )
                        else:
                            price = 0
                            if action == 'change_in_the_quantity':
                                product.update_quantity(quantity=quantity, )
                                price = product.update_price_per_piece()
                            elif action == 'change_delete':
                                product.delete()
                            response = {'product_pk': product_pk,
                                        'product_price': float(price, ),
                                        'action': action,
                                        'result': 'Ok', }
                    elif action == 'change_add':
                        order = request.POST.get(u'order_pk', None, )
                        try:
                            order = int(order, )
                        except ValueError:
                            return HttpResponse(status=400, )
                        else:
                            from apps.cart.models import Order
                            try:
                                order = Order.objects.get(pk=order, )
                            except Order.DoesNotExist:
                                print '2'
                                return HttpResponse(status=400, )
                            else:
                                from apps.product.models import Product
                                try:
                                    product = Product.objects.get(pk=product_pk, )
                                except Product.DoesNotExist:
                                    print '3'
                                    return HttpResponse(status=400, )
                                else:
                                    order, product_in_cart = order.product_add(obj_product=product, )
                        response = {'product_pk': product_in_cart.pk,
                                    'product_price': float(product_in_cart.price, ),
                                    'order_pk': order.pk,
                                    'action': action,
                                    'result': 'Ok', }
                    else:
                        print '5'
                        return HttpResponse(status=400, )
                    data = dumps(response, )
                    mimetype = 'application/javascript'
                    return HttpResponse(data, mimetype, )
            # else:
            #     print '6'
            #     return HttpResponse(status=400, )
        elif request.method == 'GET':
            return HttpResponse(status=400, )
        else:
            return HttpResponse(status=400, )
    else:
        return HttpResponse(status=400, )


""" Вызывается из админ панели. -> Добавление товара в заказ. -> Поиск товара """
def order_add_search(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            search_string = request.POST.get(u'QueryString', None, )
            # print request.POST
            if search_string:
                # len_search_string = len(search_string, )
                """ Поиск товара по полученной строке """
                from django.db.models import Q
                q = Q(name__contains=search_string)# | Q(name__contains=search_string)
                # print search_string
                from apps.product.models import Product
                try:
                    products = Product.objects.filter(q, )
                except Product.DoesNotExist:
                    products = None
                else:
                    from apps.product.models import ItemID
                    try:
                        ItemsID = ItemID.objects.filter(Q(ItemID__icontains=search_string, ), )
                    except ItemID.DoesNotExist:
                        ItemsID = None
                    else:
                        for item in ItemsID:
                            from apps.product.models import Product
                            try:
                                product = Product.objects.filter(ItemID=item, )
                            except Product.DoesNotExist:
                                pass
                            else:
                                products = product | products
                    if products:
                        results = []
                        for product in products:
                            # product_name = product.name
                            # index_search_string = product_name.find(search_string, )
                            # product_name = product_name[:index_search_string] + '<span>' + product_name[index_search_string:index_search_string+len_search_string] + '</span>' + product_name[index_search_string+len_search_string:]
                            results.append({'pk': product.pk,
                                            'name': product.name,
                                            'itemid': product.get_ItemID,
                                            'title': product.title, })
                        response = {'results': results,
                                    # 'query': 'Unit',
                                    'result': 'Ok', }
                    else:
                        response = {'result': 'Bad', }
                    # print request.REQUEST['callback']
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


def order_add(request, ):
    if request.is_ajax():
        if request.method == 'GET':
            search_string = request.session.get(u'cookie', None, )
        elif request.method == 'GET':
            return HttpResponse(status=400, )
        else:
            return HttpResponse(status=400, )
    else:
        return HttpResponse(status=400, )
