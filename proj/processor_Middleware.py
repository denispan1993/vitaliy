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
    def process_request(self, request, ):
        """ ajax_resolution """
        ajax_resolution_datetime = request.session.get(u'ajax_resolution_datetime', None, )
        from datetime import datetime, timedelta
        if not ajax_resolution_datetime or ajax_resolution_datetime < (datetime.now() - timedelta(seconds=60, )):
            request.session[u'ajax_resolution'] = True
        else:
            request.session[u'ajax_resolution'] = False
        """ ajax_cookie """
        if not "cookie" in request.session:
            request.session[u'ajax_cookie'] = True
            request.session.set_test_cookie()
        else:
            if "ajax_cookie" in request.session:
                request.session.delete_test_cookie()
                del request.session['ajax_cookie']

        if "sessionid" in request.COOKIES:
            SESSIONID_COOKIES_ = request.COOKIES['sessionid']
        else:
            SESSIONID_COOKIES_ = None

        request.SESSIONID_COOKIES_ = SESSIONID_COOKIES_
        """ Убираем ссылки на Продукт и Категорию из session """
        if u"product" in request.session:
            request.session[u'product'] = False
        if u"category" in request.session:
            request.session[u'category'] = False

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
