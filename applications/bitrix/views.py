# -*- coding: utf-8 -*-
import os
import base64
from celery.utils import uuid
from datetime import datetime, date
from django.views.generic import View
from django.http import QueryDict, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .tasks import process_bitrix_catalog

__author__ = 'AlexStarov'


#@method_decorator(csrf_exempt, name='dispatch')
class ExchangeView(View, ):

    @method_decorator(csrf_exempt, )
    def dispatch(self, request, *args, **kwargs):
        return super(ExchangeView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        auth_token_1c = request.META.get('HTTP_AUTHORIZATION', False)
        auth_token_server = 'Basic ' + base64.b64encode('User123:password123')

        if auth_token_1c == auth_token_server:

            request_COOKIES = request.COOKIES.get('sessionid', False, )
            request_COOKIES_len = len(request.COOKIES, )

            if not request_COOKIES\
                    and request_COOKIES_len == 0\
                    and not request.session.session_key:

                if not request.session.exists(request.session.session_key):
                    request.session.create()

            elif request_COOKIES == request.session.session_key:
                pass
            else:
                return HttpResponse('failure', )
        else:
            return HttpResponse('failure', )

        data = request.GET.copy()

        if data.get('type', False, ) == 'catalog':
            mode = data.get('mode', False, )

            if mode == 'checkauth':
                return HttpResponse('success\nsessionid\n{key}'.format(key=request.session.session_key), )

            elif mode == 'init':
                return HttpResponse('zip=no\nfile_limit=16777216', )

            elif mode == 'import':
                filename = data.get('filename', False, )
                if filename == 'import.xml':
                    pass
                elif filename == 'offers.xml':
                    task = process_bitrix_catalog\
                        .apply_async(
                            queue='celery',
                            task_id='celery-task-id-{0}'.format(uuid(), ), )

                return HttpResponse('success', )

        return HttpResponse('', )

    def post(self, request, *args, **kwargs):

        auth_token_1c = request.META.get('HTTP_AUTHORIZATION', False)
        auth_token_server = 'Basic ' + base64.b64encode('User123:password123')

        if auth_token_1c == auth_token_server:

            request_COOKIES = request.COOKIES.get('sessionid', False, )

            if not request_COOKIES == request.session.session_key:
                return HttpResponse('failure', )

        else:
            return HttpResponse('failure', )

        query_string = request.META.get('QUERY_STRING', False, )

        query_string = QueryDict(query_string=query_string, )

        if query_string.get('type', False, ) == 'catalog'\
                and query_string.get('mode', False, ) == 'file'\
                and request.META.get('CONTENT_TYPE', False, ) == 'application/octet-stream':

            filename = query_string.get('filename', False, )

            path = 'storage/{app}/{year}/{month:02d}/{day:02d}/'\
                .format(
                    app='bitrix',
                    year=date.today().year,
                    month=date.today().month,
                    day=date.today().day,
                )

            path_split = path.split('/', )
            path = ''
            for dir in path_split:

                path += '{dir}/'.format(dir=dir, )
                try:
                    os.stat(path, )
                except Exception as e:
                    print e
                    os.mkdir(path, )

            filename = '{filename}.{hour:02d}.{minute:02d}.{ext}'\
                .format(
                    filename=filename.split('.')[0],
                    hour=datetime.now().hour,
                    minute=datetime.now().minute,
                    ext=filename.split('.')[1],
                )
            with open('{path}{filename}'.format(path=path, filename=filename, ), 'w') as outfile:
                outfile.write(request.body)

        return HttpResponse('success', )
