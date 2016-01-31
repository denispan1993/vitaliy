# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'


def context(request, ):
    #    from apps.product.models import Category
    #    try:
    #        all_categories_ = Category.manager.published()
    #    except Category.DoesNotExist:
    #        all_categories_ = None

    #    ajax_resolution_ = request.session.get(u'ajax_resolution', True, )
    print 'Django_Context_Processor:'
    print 'print request: ', request
    if str(request, ).find('WSGIRequest:', ):
        url = str(request, ).split("'")[1]
        print url
        try:
            value = url.decode('cp1252').encode('utf8')
        except:
            pass
        else:
            try:
                print 'cp1252 -1', type(value, ), value
            except:
                print 'cp1252 -1', type(value, ), 'print value: Error'
        try:
            value = url.encode('cp1252')
        except:
            pass
        else:
            try:
                print 'cp1252 -2', type(value, ), value
            except:
                print 'cp1252 -2', type(value, ), 'print value: Error'

    try:
        url = dict(request)
        print 'dict: ', url
        url = url['WSGIRequest']
    except Exception as e:
        print 'Exception: ', e
    except TypeError as e:
        print 'TypeError: ', e
    print 'WSGIRequest: ', url
    url = request.get_full_path()
    from django.shortcuts import redirect
    # return redirect(to=url)
    from django.utils.encoding import uri_to_iri
    url = uri_to_iri(url, )
    url = url.encode('cp1252', )
    print 'Next URL: request.get_full_path: ', url
    from django.core.urlresolvers import resolve, Resolver404
    view, args, kwargs = resolve(url, )
    print view, args, kwargs
    from apps.product.views import show_product
    if 'view' in locals() and view == show_product:
        try:
            product_pk = int(kwargs[u'id'], )
        except ValueError:
            pass
        else:
            print product_pk, kwargs[u'product_url'].encode('utf8')
            from apps.product.views import get_product
            """ Убираем НАХРЕН проверку именования товара product_url """
            # product = get_product(product_pk=product_pk, product_url=kwargs[u'product_url'], )
            product = get_product(product_pk=product_pk, )
            print product
            #return redirect(to=product.get_absolute_url(), )
    #return redirect(to='http://keksik.com.ua%s' % url, )
    return dict(url=product.get_absolute_url(), )
