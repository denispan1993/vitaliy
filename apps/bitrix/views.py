# -*- coding: utf-8 -*-
from django.views.generic import View
from django.template.loader import get_template
from django.http import HttpResponse

__author__ = 'AlexStarov'


class Exchange(View, ):

    def get(self, request, *args, **kwargs):
        data = request.GET.copy()
        for key, value in data.iteritems():
            print 'key: ', key, ' value: ', value

        request_type = data.get('type', False, )

        if request_type == 'catalog':
            mode = data.get('mode', False, )

            if mode == 'checkauth':
                if not request.session.exists(request.session.session_key):
                    request.session.create()
                return HttpResponse('success\nsessionid\n{key}'.format(key=request.session.session_key), )

            elif mode == 'init':
                pass

        return HttpResponse('', )
