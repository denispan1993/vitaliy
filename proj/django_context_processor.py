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
        url = url['WSGIRequest']
    except Exception as e:
        print 'Exception: ', e
    except TypeError as e:
        print 'TypeError: ', e
    print 'WSGIRequest: ', url
    url = request.get_full_path()
    from django.utils.encoding import uri_to_iri
    url = uri_to_iri(url, )
    url = url.encode('cp1252', )
    print 'Next URL: request.get_full_path: ', url
    from django.shortcuts import redirect
    return redirect(to=url, )
    # return dict()
