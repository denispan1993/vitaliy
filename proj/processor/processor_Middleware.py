# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'


class Process_SessionIDMiddleware(object):
    def process_response(self, request, response, ):
        """
            Узнаем текущий key session.
            Он лежит именно в COOKIES.
        """
        sessionid = request.COOKIES.get('sessionid', False, )
        """
            Узнаем предыдуший key session.
            Если он конечно есть.
            А если его еще нету значит пользователь у нас впервые.
        """
        session = request.COOKIES.get('session', False, )
        """
            Проверим,
            а может пользователь у нас все же когда то был.
        """
        from applications.account.models import Session_ID
        try:
            session_ID = Session_ID.objects.get(sessionid=sessionid, )
        except Session_ID.DoesNotExist:
            from django.contrib.sessions.backends.db import SessionStore
            s = SessionStore()
            s_save = False
            from django.db import OperationalError
            while s_save:
                try:
                    s.save()
                except OperationalError:
                    print 'S.save() Error: "OperationalError: database is locked" '
                else:
                    s_save = True
            session_ID = s.session_key
        if not session and not sessionid:
            """
                Вот здесь мы будем "что-то" делать........ чтобы понять откуда пришел пользователь
                Так как он здесь впервые.
            """
            """
                Но сначал нужно сам session запомнить. Иначе нифига не будет работать.
            """
            # print u'Этот пользователь здесь впервые.'
            # print u'New User.'
            """
                Так как это самый первый вход эт ого пользователя к нам на сайт,
                то создаем для него "самую главную запись" ;-)
            """
            from django.contrib.auth import get_user_model
            UserModel = get_user_model()
            password = UserModel.objects.make_random_password()
            # user_obj = UserModel.objects.create_user(username=session_ID, email=None, password=password, )

#        user = self.model(username=username, email=email,
#                          is_staff=is_staff, is_active=True,
#                          is_superuser=is_superuser, last_login=now,
#                          date_joined=now, **extra_fields)
            # session_ID = Session_ID.objects.create(user=user_obj, sessionid=sessionid, )
            # request.session['session'] = sessionid
            response.set_cookie(key='session', value=sessionid, )
            pass
        elif not session and session_ID:
            """
                Пользователь был у нас на сайте.
                Но с тех пор почемуто исчез "наш" sesion из COOKIES.
            """
            response.set_cookie(key='session', value=sessionid, )
        elif session and session == sessionid:
            """
                Пользователь ничего не сделал.
                Можно не обращать на это внимание.
            """
            pass
        elif session and session != sessionid:
            """
                Вот тут самое интересное.
                Пользователь "изменился".
                Изменил свое "состояние".
            """
            # request.session['session'] = sessionid
            # print 'set session in COOKIES'
            response.set_cookie(key='session', value=sessionid, )
            from applications.utils.update_sessionid import update_sessionid
            update_sessionid(request, sessionid_old=session, sessionid_now=sessionid, )

        return response

    def process_request(self, request, ):
        # print 'Inter request'
        """ ajax_resolution """
        ajax_resolution_datetime = request.session.get(u'ajax_resolution_datetime', False, )
        if ajax_resolution_datetime:
            # import django
            # django_version = django.VERSION
            # if int(django_version[0], ) == 1 and int(django_version[1], ) >= 6:
            from django.utils.dateparse import parse_datetime
            ajax_resolution_datetime = parse_datetime(ajax_resolution_datetime, )
            # elif int(django_version[0], ) == 1 and int(django_version[1], ) == 5:
            #     ajax_resolution_datetime = ajax_resolution_datetime
            from datetime import datetime, timedelta
            if not ajax_resolution_datetime or \
               ajax_resolution_datetime < (datetime.now() - timedelta(seconds=10, )):
                request.session[u'ajax_resolution'] = True
            else:
                request.session[u'ajax_resolution'] = False
        else:
            request.session[u'ajax_resolution'] = True
        """ ajax_timezone """
        ajax_timezone_datetime = request.session.get(u'ajax_timezone_datetime', False, )
        if ajax_timezone_datetime:
            from django.utils.dateparse import parse_datetime
            ajax_timezone_datetime = parse_datetime(ajax_timezone_datetime, )
            from datetime import datetime, timedelta
            if not ajax_timezone_datetime or \
               ajax_timezone_datetime < (datetime.now() - timedelta(seconds=86400, )):
                request.session[u'ajax_timezone'] = True
            else:
                request.session[u'ajax_timezone'] = False
        else:
            request.session[u'ajax_timezone'] = True
        """ ajax_geoip """
        ajax_geoip_datetime = request.session.get(u'ajax_geoip_datetime', False, )
        if ajax_geoip_datetime:
            from django.utils.dateparse import parse_datetime
            ajax_geoip_datetime = parse_datetime(ajax_geoip_datetime, )
            from datetime import datetime, timedelta
            if not ajax_geoip_datetime or \
               ajax_geoip_datetime < (datetime.now() - timedelta(seconds=86400, )):
                request.session[u'ajax_geoip'] = True
            else:
                request.session[u'ajax_geoip'] = False
        else:
            request.session[u'ajax_geoip'] = True
        """ reclame """
        reclame_datetime = request.session.get(u'reclame_datetime', False, )
        ajax_geoip_city = request.session.get(u'ajax_geoip_city', False, )
        from datetime import datetime, timedelta
        if reclame_datetime and\
                        ajax_geoip_city == u'\u041d\u0438\u043a\u043e\u043b\u0430\u0435\u0432':
            from django.utils.dateparse import parse_datetime
            reclame_datetime = parse_datetime(reclame_datetime, )
            if not reclame_datetime or \
               reclame_datetime < (datetime.now() - timedelta(seconds=86400, )):
                request.session[u'reclame'] = True
                request.session[u'reclame_datetime'] = str(datetime.now(), )
            else:
                request.session[u'reclame'] = False
        elif not reclame_datetime and\
                        ajax_geoip_city == u'\u041d\u0438\u043a\u043e\u043b\u0430\u0435\u0432':
            request.session[u'reclame'] = True
            request.session[u'reclame_datetime'] = str(datetime.now(), )
        """ withs and right_panel """
        explorer_with = request.session.get(u'width', None, )
        if explorer_with:
            request.session[u'right_panel'] = True
            try:
                explorer_with = int(explorer_with, )
            except ValueError:
                request.session[u'width_main_center'] = 960
                request.session[u'limit_on_string'] = 4
                request.session[u'limit_on_page'] = 12
                # request.session[u'test_on_with'] = u'Bad'
            else:
                # del request.session[u'test_on_with']
                # limit = 12 if explorer_with >= 984 else limit = 9
                if explorer_with >= 1700:
                    request.session[u'width_main_center'] = 1192
                    request.session[u'limit_on_string'] = 5
                    request.session[u'limit_on_page'] = 15
                    request.session[u'width_this_category'] = 972
                elif explorer_with >= 1450:
                    request.session[u'width_main_center'] = 960
                    request.session[u'limit_on_string'] = 4
                    request.session[u'limit_on_page'] = 12
                    request.session[u'width_this_category'] = 732
                elif explorer_with >= 1210:
                    request.session[u'width_main_center'] = 720
                    request.session[u'limit_on_string'] = 3
                    request.session[u'limit_on_page'] = 9
                    request.session[u'width_this_category'] = 492
                elif explorer_with >= 960:
                    request.session[u'width_main_center'] = 480
                    request.session[u'limit_on_string'] = 2
                    request.session[u'limit_on_page'] = 6
                    request.session[u'width_this_category'] = 252
                elif explorer_with > 480:
                    request.session[u'width_main_center'] = 480
                    request.session[u'limit_on_string'] = 2
                    request.session[u'limit_on_page'] = 6
                    request.session[u'width_this_category'] = 252
                    request.session[u'right_panel'] = False
                elif explorer_with <= 480:
                    request.session[u'width_main_center'] = 240
                    request.session[u'limit_on_string'] = 1
                    request.session[u'limit_on_page'] = 3
                    request.session[u'width_this_category'] = 252
                    request.session[u'right_panel'] = False
        else:
            # request.session[u'test_on_with'] = u'Bad get'
            request.session[u'width_main_center'] = 960
            request.session[u'limit_on_string'] = 4
            request.session[u'limit_on_page'] = 12

        """ ajax_cookie """
        if not "cookie" in request.session:
            request.session[u'ajax_cookie'] = True
            request.session.set_test_cookie()
        else:
            if "ajax_cookie" in request.session:
                request.session.delete_test_cookie()
                del request.session['ajax_cookie']

        """ Убираем ссылки на Продукт и Категорию из session """
        if u'product' in request.session:
            del request.session[u'product']  # = False
        if u'category' in request.session:
            del request.session[u'category']  # = False
