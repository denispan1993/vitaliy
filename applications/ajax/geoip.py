# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

try:
    from django.utils.simplejson import dumps
    # import simplejson as json
except ImportError:
    from json import dumps
    # import json

from django.http import HttpResponse


def resolve_client_geolocation(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            response = {'result': 'Ok', }
            # request.session[u'ajax_timezone'] = True
            #ajax_timezone_offset = request.session.get(u'ajax_timezone_offset', False, )
            #request.session[u'ajax_timezone_offset'] = ajax_timezone_offset
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[-1].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            if ip != '127.0.0.1':
                param = {'ip': ip, }
                from requests import get
                # r = get(url='http://ipgeobase.ru:7020/geo', params=param, )
                r = get(url='http://194.85.91.253:7020/geo', params=param, )
                from xml.etree import cElementTree
                e = cElementTree.XML(r.text.encode('cp1251', errors='replace', ), )
                #print e
                #d = etree_to_dict(e, )
                #print d
                try:
                    # city = d['ip-answer']['ip']['city']
                    city = e[0][2].text
                    region = e[0][3].text
                    print('e[0][2].text - ', 'r.url: ', r.url, ' City: ', city.encode('utf-8', ),
                          ' Region: ', e[0][3].text.encode('utf-8', ), )
                # except KeyError:
                except IndexError:
                    # city = d['ip-answer']['ip']['message']
                    city = e[0][0].text
                    region = e[0][0].text
                    print('e[0][0].text - ', 'r.url: ', r.url, ' City: ', city.encode('utf-8', ), )

                request.session[u'ajax_geoip_city'] = city
                request.session[u'ajax_geoip_region'] = region
            from datetime import datetime
            request.session[u'ajax_geoip_datetime'] = str(datetime.now(), )
            # response = {'result': 'Please enable cookies and try again.', }
            # request.session[u'cookie'] = False
            data = dumps(response, )
            mimetype = 'application/javascript'
            return HttpResponse(data, mimetype, )
        elif request.method == 'GET':
            return HttpResponse(status=400, )
        else:
            return HttpResponse(status=400, )
    else:
        return HttpResponse(status=400, )


def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        from collections import defaultdict
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.iteritems():
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d
