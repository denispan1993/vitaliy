# coding=utf-8
#import time
#from django.conf import settings
#from django.utils.cache import patch_vary_headers
#from django.utils.http import cookie_date
#from django.utils.importlib import import_module
##from django.core.context_processors import csrf
#from django.conf import settings
##from django.core.urlresolvers import reverse
#from django.http import HttpResponse, HttpResponseRedirect
#from django.shortcuts import render_to_response
##from django.template import RequestContext
#from django.contrib.sessions.models import Session
#from django.contrib.auth.models import User
##from django.contrib.sites.models import Site
#from django.forms.models import modelformset_factory
##from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, Select

##from registration.forms import RegistrationForm, RegistrationFormUniqueEmail, ProfileForm
##from database_products.forms import ColorsForm, SizesForm
#from Carts.models import Carts, More_Options_Carts
#from database_products.models import database_products, Last_viewed
#from database_products.views import _cart_id #views_price_per_piece, 
#from Manufacturers.models import Manufacturers, Countrys
#from database_products.models import Rubrics, Categories, database_products, Views, Colors_m2m, Colors, Sizes_m2m, Sizes


class Process_SessionIDMiddleware(object):
    def process_response(self, request, response, ):
        # print 'Cookie'
        """
            Узнаем текущий key session.
            Он лежит именно в COOKIES.
        """
        sessionid = request.COOKIES.get('sessionid', False, )
        # print 'sessionid: ', sessionid
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
        from apps.account.models import Session_ID
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
                    # pass
                else:
                    s_save = True
            session_ID = s.session_key
        # print 'session: ', session
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
            from apps.utils.update_sessionid import update_sessionid
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
               ajax_resolution_datetime < (datetime.now() - timedelta(seconds=120, )):
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
                request.session[u'width_main_center'] = 950
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
                    request.session[u'width_main_center'] = 951
                    request.session[u'limit_on_string'] = 4
                    request.session[u'limit_on_page'] = 12
                    request.session[u'width_this_category'] = 732
                elif explorer_with >= 1210:
                    request.session[u'width_main_center'] = 711
                    request.session[u'limit_on_string'] = 3
                    request.session[u'limit_on_page'] = 9
                    request.session[u'width_this_category'] = 492
                elif explorer_with >= 960:
                    request.session[u'width_main_center'] = 470
                    request.session[u'limit_on_string'] = 2
                    request.session[u'limit_on_page'] = 6
                    request.session[u'width_this_category'] = 252
                elif explorer_with < 960:
                    request.session[u'width_main_center'] = 470
                    request.session[u'limit_on_string'] = 2
                    request.session[u'limit_on_page'] = 6
                    request.session[u'width_this_category'] = 252
                    request.session[u'right_panel'] = False
        else:
            # request.session[u'test_on_with'] = u'Bad get'
            request.session[u'width_main_center'] = 950
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

#        from apps.cart.models import Cart
#        try:
#            cart_all = Cart.objects.all()
#        except Cart.DoesNotExist:
#            pass
#        else:
#            print cart_all
#            try:
#                print cart_all[0]
#                print cart_all[0].session.session_key
#            except IndexError:
#                pass



            #        ajax_resolution_datetime = request.session.get(u'ajax_resolution_datetime', None, )
#        from datetime import datetime, timedelta
#        if not ajax_resolution_datetime or ajax_resolution_datetime < (datetime.now() - timedelta(hours=1, )):
#            request.session[u'ajax_resolution'] = True
#        else:
#            request.session[u'ajax_resolution'] = False
        # curent_category

##        cartid = _cart_id(request)
#        CHANGED_ = False
#        AUTH_ = False
##        user_object_ = None
#        if "AUTH_" in request.session:
#            AUTH_ = request.session['AUTH_']
#        if not request.user.is_authenticated() and AUTH_ == True:
#            CHANGED_ = True
#            request.session['CHANGED_'] = True
#        if not request.user.is_authenticated():
#            AUTH_ = False
#            request.session['AUTH_'] = False
#        if request.user.is_authenticated() and request.user.is_active and AUTH_ == False:
#            CHANGED_ = True
#            request.session['CHANGED_'] = True
#        if request.user.is_authenticated() and request.user.is_active:
#            user_id_ = request.session['_auth_user_id']
#            user_object_ = User.objects.get(pk=user_id_)
#            AUTH_ = True
#            request.session['AUTH_'] = True
#        else:
#            user_object_ = None
#        if request.session.test_cookie_worked():
#            if "sessionid" in request.COOKIES:
#                SESSIONID_COOKIES_ = request.COOKIES['sessionid']
#                if "SESSIONID_" in request.session:
#                    SESSIONID_SESSION_ = request.session['SESSIONID_']
#                    if SESSIONID_COOKIES_ != SESSIONID_SESSION_ and CHANGED_ == True:
#                        if "SESSIONID_VERY_OLD_" in request.session:
#                            SESSIONID_SESSION_OLD_ = request.session['SESSIONID_VERY_OLD_']
#                            request.session['SESSIONID_VERY_OLD_'] = SESSIONID_SESSION_OLD_
#                        else:
 #                           SESSIONID_SESSION_OLD_ = None
 #                           request.session['SESSIONID_VERY_OLD_'] = None
 #                       request.session['SESSIONID_'] = SESSIONID_COOKIES_
 #                       request.session['SESSIONID_OLD_'] = SESSIONID_SESSION_
 #                   else:
#                        SESSIONID_SESSION_OLD_ = None
#                else:
#                    request.session['SESSIONID_'] = SESSIONID_COOKIES_
#                    SESSIONID_SESSION_ = None
#                    SESSIONID_SESSION_OLD_ = None
#            else:
#                SESSIONID_COOKIES_ = None
#                SESSIONID_SESSION_ = None
#                SESSIONID_SESSION_OLD_ = None
#        else:
#            SESSIONID_COOKIES_ = None
#            SESSIONID_SESSION_ = None
#            SESSIONID_SESSION_OLD_ = None

#        if CHANGED_ != True:
#            request.session['CHANGED_'] = False
#        else:
#            if request.user.is_authenticated() and request.user.is_active:
#                last_viewed = Last_viewed.objects.filter(user_obj=None, sessionid=SESSIONID_SESSION_, ).update(user_obj=user_object_, sessionid=None, )
#                try:
#                    user_carts = Carts.objects.filter(user_obj=user_object_, sessionid=None, order=None, account=None, package=None, ) #cartid=cartid,
#                except:
#                    user_carts = None
#                try:
#                    sessionid_carts = Carts.objects.filter(user_obj=None, sessionid=SESSIONID_SESSION_, order=None, account=None, package=None, ) #cartid=cartid,
#                except:
#                    sessionid_carts = None
#                if user_carts == None and sessionid_carts == None:
#                    # Вообще ничего не делать
#                    pass
#                if user_carts != None and sessionid_carts == None:
#                    # Тоже ничего не делать
#                    pass
#                if user_carts == None and sessionid_carts != None:
#                    # Самый простой случай, преобразуем все упоминания в корзине неизвестного пользователя (SESSIONID) в известного пользователя (user_obj)
#                    Carts.objects.filter(user_obj=None, sessionid=SESSIONID_SESSION_, account=None, package=None, ).update(user_obj=user_object_, sessionid=None, ) #cartid=cartid,
#                if user_carts != None and sessionid_carts != None:
#                    # Самый сложный случай, сращиваем деревья.
#                    for sessionid_cart in sessionid_carts:
#                        try:
#                            user_cart = user_carts.get(user_obj=user_object_, sessionid=None, product=sessionid_cart.product, ) #cartid=cartid,
#                            if user_cart.id:
#                                #Если ДА, то все очень плохо.
#                                user_cart_options = user_cart.cart.all()
#                                sessionid_cart_options = sessionid_cart.cart.all()
#                                for sessionid_cart_option in sessionid_cart_options:
#                                    try:
#                                        user_cart_option = user_cart_options.get(color=sessionid_cart_option.color, size=sessionid_cart_option.size,  ) #cart=user_cart,
#                                        if user_cart_option.id:
#                                            #Если ДА, то хуже уже некуда.
#                                            user_cart_option.update_quantity(sessionid_cart_option.quantity)
#                                            user_cart_option.update_price_per_piece()
#                                            sessionid_cart_option.delete()
#                                        else:
#                                            #Если НЕТ, то хуже еще есть куда.
#                                            sessionid_cart_option.cart = user_cart
#                                            sessionid_cart_option.save()
#                                    except More_Options_Carts.DoesNotExist:
#                                        #Если НЕТ, то хуже еще есть куда.
#                                        sessionid_cart_option.cart = user_cart
#                                        sessionid_cart_option.save()
#                            else:
#                                #Если НЕТ, то все немного проще.
#                                sessionid_cart.user_obj = user_object_
#                                sessionid_cart.sessionid = None
#                                sessionid_cart.save()
#                        except Carts.DoesNotExist:
#                            #Если НЕТ, то все немного проще.
#                            sessionid_cart.user_obj = user_object_
#                            sessionid_cart.sessionid = None
#                            sessionid_cart.save()
#            else:
##                last_viewed = Last_viewed.objects.filter(user_obj=user_object_, sessionid=None, ).update(user_obj=None, sessionid=SESSIONID_COOKIES_, )
#                pass

#        request.SESSIONID_COOKIES_ = SESSIONID_COOKIES_
#        request.SESSIONID_SESSION_ = SESSIONID_SESSION_
#        request.SESSIONID_SESSION_OLD_ = SESSIONID_SESSION_OLD_
#        request.CHANGED_ = CHANGED_
#        request.AUTH_ = AUTH_
##        request.cartid_ = cartid
#        request.user_object_ = user_object_
#        request.IP_ADDRESS_ = request.META['REMOTE_ADDR']

#    def process_template_response(self, request, response):
#        request.aaabbb_ = 1
#        return response

#class SessionMiddleware(object):
#    def process_request(self, request):
#        engine = import_module(settings.SESSION_ENGINE)
#        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
#        request.session = engine.SessionStore(session_key)

#def price_per_piece(product=None, quantity=1):
#    price_per_piece = product.price
#    try:
#        discounts = product.discounts.order_by('quantity_of_products').all()
#        if discounts != None and discounts.count() > 0 and quantity >1:
#            for discount in discounts:
#                if discount.quantity_of_products <= quantity:
#                    price_per_piece = discount.price
#    except: pass

#    return price_per_piece



















#                        exist_sessionid_carts = Carts.objects.filter(user_obj=None, sessionid=SESSIONID_SESSION_, )
#                        for exist_user_cart in exist_user_carts:
#                            exist_sessionid_cart = exist_sessionid_carts.get(product=exist_user_cart.product, )
#                            if exist_sessionid_cart != None:
#                                exist_user_cart_options = exist_user_cart.cart.all()
#                                exist_i = exist_user_cart_options.count()
#                                i = 0
#                                exist_sessionid_cart_options = exist_sessionid_cart.cart.all()
#                                for exist_user_cart_option in exist_user_cart_options:
#                                    i += 1
#                                    try:
#                                        if exist_sessionid_cart.id:
#                                            exist_sessionid_cart_option = exist_sessionid_cart.cart.get(color=exist_user_cart_option.color, size=exist_user_cart_option.size, )
#                                            if exist_sessionid_cart_option != None:
#                                                try:
#                                                    product = database_products.objects.get(pk=exist_user_cart.product_id, )
#                                                    quantity = exist_user_cart_option.quantity + exist_sessionid_cart_option.quantity
#                                                    price_per_piece = views_price_per_piece(product=product, quantity=quantity, )
#                                                    exist_new_option = More_Options_Carts.objects.filter(pk=exist_user_cart_option.id).update(price_per_piece=price_per_piece, quantity=quantity, sum_of_quantity=price_per_piece*quantity, color=exist_user_cart_option.color, size=exist_user_cart_option.size, )
#                                                    if exist_sessionid_cart_options.count() <=1:
#                                                        exist_sessionid_cart.delete()
#                                                        exist_sessionid_cart_option.delete()
#                                                    else:
#                                                        exist_sessionid_cart_option.delete()
#                                                except database_products.DoesNotExist:
#                                                    pass
#                                    except More_Options_Carts.DoesNotExist:
#                                        for exist_sessionid_cart_option in exist_sessionid_cart_options:
#                                            exist_sessionid_cart = Carts.objects.get(sessionid=SESSIONID_SESSION_, product=exist_user_cart.product, )
#                                            exist_sessionid_cart_options = exist_sessionid_cart.cart.all()
#                                            if exist_sessionid_cart_options.count() > 1:
#                                                pass
##                                                exist_user_cart.more_options.add(exist_sessionid_cart_option)
##                                                exist_user_cart.save()
##                                                exist_sessionid_cart.more_options.remove(exist_sessionid_cart_option)
##                                                exist_sessionid_cart.save()
##                                                exist_sessionid_cart_option.delete()
#                                            else:
#                                                pass
##                                                exist_user_cart.more_options.add(exist_sessionid_cart_option)
##                                                exist_user_cart.save()
#                                                exist_sessionid_cart.delete()
#                                        pass
#                                    if i == exist_i and exist_sessionid_cart_options.count() > 0:
#                                        exist_sessionid_cart = Carts.objects.get(sessionid=SESSIONID_SESSION_, product=exist_user_cart.product, )
#                                        exist_sessionid_cart_options = exist_sessionid_cart.cart.all()
#                                        for exist_sessionid_cart_option in exist_sessionid_cart_options:
#                                            if exist_sessionid_cart_options.count() > 0:
##                                                exist_user_cart = Carts.objects.get(user_obj=user_object_, sessionid=None, product=exist_user_cart.product, )
#                                                exist_sessionid_cart_option.update(product=exist_user_cart, )
#                                                pass
#                                            else:
#                                                exist_sessionid_cart.delete()


#                    except Carts.DoesNotExist:
#                        pass
                            
#                except Carts.DoesNotExist:
#                    pass
#                try:
#                    exist_sessionid_carts = Carts.objects.filter(sessionid=SESSIONID_SESSION_, ).update(user_obj=user_object_, sessionid=None, )
#                except Carts.DoesNotExist:
#                    pass


#                   try:
#                        exist_sessionid_carts = Carts.objects.filter(user_obj=None, sessionid=SESSIONID_SESSION_, )
#                        for exist_user_cart in exist_user_carts:
#                            exist_sessionid_cart = exist_sessionid_carts.get(product=exist_user_cart.product, )
#                            if exist_sessionid_cart != None:
#                                exist_user_cart_options = exist_user_cart.cart.all()
#                                exist_i = exist_user_cart_options.count()
#                                i = 0
#                                exist_sessionid_cart_options = exist_sessionid_cart.cart.all()
#                                for exist_user_cart_option in exist_user_cart_options:
#                                    i += 1
#                                    try:
#                                        if exist_sessionid_cart.id:
#                                            exist_sessionid_cart_option = exist_sessionid_cart.cart.get(color=exist_user_cart_option.color, size=exist_user_cart_option.size, )
#                                            if exist_sessionid_cart_option != None:
#                                                try:
##                                                    product = database_products.objects.get(pk=exist_user_cart.product_id, )
#                                                    quantity = exist_user_cart_option.quantity + exist_sessionid_cart_option.quantity
#                                                    price_per_piece = views_price_per_piece(product=exist_user_cart.product, quantity=quantity, )
#                                                    More_Options_Carts.objects.filter(pk=exist_user_cart_option.id).update(price_per_piece=price_per_piece, quantity=quantity, sum_of_quantity=price_per_piece*quantity, )
#                                                    if exist_sessionid_cart_options.count() <=1:
#                                                        exist_sessionid_cart.delete()
#                                                        exist_sessionid_cart_option.delete()
#                                                    else:
#                                                        exist_sessionid_cart_option.delete()
#                                                except database_products.DoesNotExist:
#                                                    pass
#                                    except More_Options_Carts.DoesNotExist:
#                                        for exist_sessionid_cart_option in exist_sessionid_cart_options:
##                                            exist_sessionid_cart = Carts.objects.get(sessionid=SESSIONID_SESSION_, product=exist_user_cart.product, )
##                                            exist_sessionid_cart_options = exist_sessionid_cart.cart.all()
#                                            if exist_sessionid_cart_options.count() > 1:
#                                                pass
##                                                exist_user_cart.more_options.add(exist_sessionid_cart_option)
##                                                exist_user_cart.save()
#                                                More_Options_Carts.objects.filter(pk=exist_sessionid_cart_option.id).update(product=, price_per_piece=price_per_piece, quantity=quantity, sum_of_quantity=price_per_piece*quantity, )
#                                            else:
#                                                pass
##                                                exist_user_cart.more_options.add(exist_sessionid_cart_option)
##                                                exist_user_cart.save()
#                                                exist_sessionid_cart.delete()
#                                        pass
#                                    if i == exist_i and exist_sessionid_cart_options.count() > 0:
#                                        exist_sessionid_cart = Carts.objects.get(sessionid=SESSIONID_SESSION_, product=exist_user_cart.product, )
#                                        exist_sessionid_cart_options = exist_sessionid_cart.cart.all()
#                                        for exist_sessionid_cart_option in exist_sessionid_cart_options:
#                                            if exist_sessionid_cart_options.count() > 0:
##                                                exist_user_cart = Carts.objects.get(user_obj=user_object_, sessionid=None, product=exist_user_cart.product, )
#                                                exist_sessionid_cart_option.update(product=exist_user_cart, )
#                                                pass
#                                            else:
#                                                exist_sessionid_cart.delete()


#                    except Carts.DoesNotExist:
#                        pass
#                            
#                except Carts.DoesNotExist:
#                    pass
#                try:
#                    exist_sessionid_carts = Carts.objects.filter(sessionid=SESSIONID_SESSION_, ).update(user_obj=user_object_, sessionid=None, )
#                except Carts.DoesNotExist:
#                    pass
