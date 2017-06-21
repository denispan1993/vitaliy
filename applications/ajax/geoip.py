# -*- coding: utf-8 -*-

try:
    from django.utils.simplejson import dumps
except ImportError:
    from json import dumps

from requests import get
from xml.etree import cElementTree
from django.http import HttpResponse
from datetime import datetime
from collections import defaultdict

__author__ = 'AlexStarov'


def resolve_client_geolocation(request, ):
    if request.is_ajax():
        if request.method == 'POST':
            response = {'result': 'Ok', }
            # request.session[u'ajax_timezone'] = True
            #ajax_timezone_offset = request.session.get(u'ajax_timezone_offset', False, )
            #request.session[u'ajax_timezone_offset'] = ajax_timezone_offset
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

            ip = x_forwarded_for.split(',')[-1].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')

            if ip != '127.0.0.1':
                # r = get(url='http://ipgeobase.ru:7020/geo', params=param, )
                r = get(url='http://194.85.91.253:7020/geo', params={'ip': ip, }, )
                e = cElementTree.XML(r.text.encode('cp1251', errors='replace', ), )
                #d = etree_to_dict(e, )
                #print d
                try:
                    # city = d['ip-answer']['ip']['city']
                    string = 'e[0][2]'
                    city = e[0][2].text
                    region = e[0][3].text
                except IndexError:
                    # city = d['ip-answer']['ip']['message']
                    string = 'e[0][0]'
                    city = e[0][0].text
                    region = e[0][0].text

                print(string, '.text - ', 'r.url: ', r.url, ' City: ', str(city.encode('utf-8', ), ),
                      ' Region: ', str(region.encode('utf-8', ), ), )

                request.session[u'ajax_geoip_city'] = city
                request.session[u'ajax_geoip_region'] = region

            request.session[u'ajax_geoip_datetime'] = str(datetime.now(), )

            return HttpResponse(dumps(response, ), 'application/javascript', )

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
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.iteritems():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
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
