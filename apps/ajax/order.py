# -*- coding: utf-8 -*-
__author__ = 'Alex Starov'

try:
    from django.utils.simplejson import dumps
    # import simplejson as json
except ImportError:
    from json import dumps
    # import json

from django.http import HttpResponse


def order_email_test(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            request_cookie = request.session.get(u'cookie', None, )
            if request_cookie:
                email = request.POST.get(u'value', None, )
                if email:
                    email = email.strip()
                    # from proj.settings import SERVER
                    # if SERVER or not SERVER:
                    is_validate = False
                    email_error = False
                    from django.core.validators import validate_email
                    from django.core.exceptions import ValidationError
                    try:
                        validate_email(email)
                    except ValidationError:
                        email_error = u'Вы допустили ошибку при наборе Вашего E-Mail адреса'
                    # else:
                        # from validate_email import validate_email
                        """ Какого-то хрена не срабаоывает проверка на MX записи. Пример lana24680@rambler.ru """
                        """ Проверка выключена """
                        # is_validate = validate_email(email, check_mx=True, verify=False, )
                        #if not is_validate:
                        #    email_error = u'Сервер указанный в Вашем E-Mail - ОТСУТСВУЕТ !!!'
                        #else:
                        #    is_validate = True

                        # if is_validate:
                        #     """ Если проверка на существование сервера прошла...
                        #         То делаем полную проверку адреса на существование... """
                        #     is_validate = validate_email(email, verify=True, )
                        #     if not is_validate:
                        #         email_error = u'Ваш E-Mail адрес не существует.'
                        # else:
                        #     email_error = u'Сервер указанный в Вашем E-Mail - ОТСУТСВУЕТ !!!'
                    # if is_validate:
                    if not email_error:
                        response = {'result': 'Ok', }
                        data = dumps(response, )
                        mimetype = 'application/javascript'
                        return HttpResponse(data, mimetype, )
                    else:
                        response = {'result': 'Bad',
                                    'email_error': email_error, }
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


from apps.product.models import Product


def products(products=Product.objects.none(),
             products_count=0,
             all_products_count=0, ):
    from apps.product.models import Product
    products_list_pk = set()
    from random import randint
    for i in range(0, products_count, ):
        product_pk = randint(1, all_products_count, )
        products_list_pk.add(product_pk, )
    return Product.objects.filter(pk__in=products_list_pk, )
#        try:
#            product = Product.objects.get(pk=product_pk, )
#        except Product.DoesNotExist:
#            pass
#        else:
#            products = products | product
#    return products
