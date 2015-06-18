# -*- coding: utf-8 -*-
__author__ = 'Alex Starov'

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
                height_visible_part_of_window = request.POST.get(u'height_visible_part_of_window', None, )
                main_left_Height = request.POST.get(u'main_left_Height', None, )
                main_center_Height = request.POST.get(u'main_center_Height', None, )
                if main_left_Height:
                    main_left_Height = int(main_left_Height, ) + 250
                if main_center_Height:
                    main_center_Height = int(main_center_Height, )
                lambda_Height = 0
                product_block_count = 0
                if main_center_Height > main_left_Height:
                    from math import floor
                    lambda_Height = main_center_Height - main_left_Height
                    if lambda_Height > height_visible_part_of_window:
                        lambda_Height = height_visible_part_of_window
                    product_block_count = int(floor(lambda_Height/300, ), )
                if product_block_count > 0 and url_path:
                    print url_path
                    if url_path == '/':
                        from apps.product.models import Product
                        qs_products = Product.objects.none()
                        try:
                            all_products_count = Product.objects.count()
                        except Product.DoesNotExist:
                            all_products_count = 0
                        else:
                            while len(qs_products, ) != product_block_count:
                                qs_products = products(products=qs_products,
                                                       products_count=product_block_count,
                                                       all_products_count=all_products_count, )
                                # print qs_products, len(qs_products, )
                            from apps.product.templatetags.blocks import many_blocks
                            html_block = many_blocks(category_or_product='product',
                                                     blocks=qs_products,
                                                     top_border=False,
                                                     limit_on_string=1,
                                                     attachment='left',
                                                     request=request, )
                response = {'result': 'Ok',
                            'url_path': url_path,
                            'lambda_Height': lambda_Height,
                            'product_block_count': product_block_count,
                            'html_block': html_block,
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
