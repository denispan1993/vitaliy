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
                r = get(url='http://ipgeobase.ru:7020/geo', params=param, )
                from xml.etree import cElementTree as ET
                e = ET.XML(r.text.encode('cp1251', ), )
                d = etree_to_dict(e, )
                print e
                print d
                print r.text
                try:
                    city = d['ip-answer']['ip']['city']
                except KeyError:
                    city = d['ip-answer']['ip']['message']

                request.session[u'ajax_geoip_city'] = city
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