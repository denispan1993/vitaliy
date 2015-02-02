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
                url_path = request.POST.get(u'url_path', None, )
                main_left_Height = request.POST.get(u'main_left_Height', None, )
                main_center_Height = request.POST.get(u'main_center_Height', None, )
                if main_left_Height:
                    main_left_Height = int(main_left_Height, )
                if main_center_Height:
                    main_center_Height = int(main_center_Height, )
                lambda_Height = 0
                product_block_count = 0
                if main_center_Height > main_left_Height:
                    from math import floor
                    lambda_Height = main_center_Height - main_left_Height
                    product_block_count = floor(lambda_Height/300, )
                if product_block_count > 0 and url_path:
                    if url_path == '/':
                        dict_products = []
                        from apps.product.models import Product
                        try:
                            all_products_count = Product.objects.count()
                        except Product.DoesNotExist:
                            all_products_count = 0
                        else:
                            while len(dict_products, ) != product_block_count:
                                dict_products = products(products=dict_products,
                                                         products_count=product_block_count,
                                                         all_products_count=all_products_count, )
                response = {'result': 'Ok',
                            'url_path': url_path,
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


def products(products=[], products_count=0, all_products_count=0, ):
    from apps.product.models import Product
    from random import randint
    for i in range(0, products_count, ):
        product_pk = randint(1, all_products_count, )
        try:
            product = Product.objects.get(pk=product_pk, )
        except Product.DoesNotExist:
            pass
        else:
            products = products + product
    return products