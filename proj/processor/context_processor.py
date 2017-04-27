# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, Resolver404
from django.core.cache import cache

from apps.cart.order import get_cart_or_create
from apps.product.models import Category, Currency
from apps.product.views import show_category, show_product, get_product, get_category, get_or_create_Viewed
from apps.slide.models import Slide
from apps.static.models import Static

__author__ = 'AlexStarov'


def context(request):

    return_dict = dict()

    try:
        static_pages = Static.objects.all()
    except Static.DoesNotExist:
        static_pages = None

    currency = cache.get(key='currency_all', )

    if not currency:

        try:
            currency = Currency.objects.all()
            cache.set(
                key='currency_all',
                value=currency,
                timeout=3600, )  # 60 sec * 60 min
        except Currency.DoesNotExist:
            currency = None

    """ Проверяем session на наличие currency pk """
    currency_pk = request.session.get(u'currency_pk', None, )
    try:
        current_currency = currency.filter(pk=currency_pk, )[0]
    except (Currency.DoesNotExist, ValueError, IndexError):
        current_currency = currency.filter(pk=1, )[0]
        request.session[u'currency_pk'] = 1

    """ Слайды """
    slides = cache.get(key='slides_visible', )

    if not slides:
        try:
            slides = Slide.manager.visible()
            cache.set(
                key='slides_visible',
                value=slides,
                timeout=3600, )  # 60 sec * 60 min

        except Slide.DoesNotExist:
            slides = None

    """ Категории верхнего уровня """
    categories_basement = cache.get(key='categories_basement', )

    if not categories_basement:
        try:
            categories_basement = Category.objects.basement()
            cache.set(
                key='categories_basement',
                value=categories_basement,
                timeout=3600, )  # 60 sec * 60 min
        except Category.DoesNotExist:
            pass

    """ Категории НЕ верхнего уровня """
#    categories_not_basement = cache.get(key='categories_not_basement', )

#    if not categories_not_basement:
#        try:
#            categories_not_basement = Category.objects.not_basement()
#            cache.set(
#                key='categories_not_basement',
#                value=categories_not_basement,
#                timeout=3600, )  # 60 sec * 60 min
#        except Category.DoesNotExist:
#            pass

    if request.user.is_authenticated() and request.user.is_active:
        user_id_ = request.session.get(u'_auth_user_id', None, )
        # from django.contrib.auth.models import User
        UserModel = get_user_model()
        try:
            user_id_ = int(user_id_, )
            user_object = UserModel.objects.get(pk=user_id_, )
        except ValueError:
            user_object = None

    else:
        user_object = None

    user_cart = get_cart_or_create(request, user_object=user_object, created=False, )

    if user_cart:
        coupons = user_cart.Cart_child.all()
        """ Проверяем СПИСОК [] на пустоту """
        if coupons:
            coupon = coupons[0]
        else:
            coupon = None

    else:
        coupon = None


    #                    sessionid_carts = Carts.objects.filter(user_obj=None, sessionid=SESSIONID_SESSION_,
    #  order=None, account=None, package=None, ) #cartid=cartid,
    #                except:
    #                    sessionid_carts = None

    # #viewed_count = viewed.count()
    # product = None
    # product_pk = None
    # from apps.product.models import Product
    # try:
    #     product_count = Product.objects.count()
    # except Product.DoesNotExist:
    #     pass
    # else:
    #     if product_count > 0:
    #         from random import randint
    #         product_pk = randint(1, product_count, )
    #         try:
    #             product = Product.objects.get(pk=product_pk, )
    #         except Product.DoesNotExist:
    #             pass

    if not request.method == 'GET':
        print 'request.method', request.method
    else:
        if user_object:
            full_path = request.path

            """ Оказывается get_full_path() возвращает полный путь со строкой запроса в случае запроса типа GET
                и долбанный resolve не может её тогда обработать и вываливается с кодом 404.
            """
            try:
                """ Вот где выскакивает эта ошибка """
                # print 'HTTP_ACCEPT: ', request.META.get('HTTP_ACCEPT', None, )
                # print 'HTTP_ACCEPT_ENCODING: ', request.META.get('HTTP_ACCEPT_ENCODING', None, )
                # print 'HTTP_ACCEPT_LANGUAGE: ', request.META.get('HTTP_ACCEPT_LANGUAGE', None, )
                # print 'LANG: ', request.META.get('LANG', None, )
                # print 'LANGUAGE: ', request.META.get('LANGUAGE', None, )
                # print 'PYTHONIOENCODING: ', request.META.get('PYTHONIOENCODING', None, )
                # print 'REQUEST_METHOD: ', request.META.get('REQUEST_METHOD', None, )
                print 'resolve:'
                view, args, kwargs = resolve(full_path, )

            except UnicodeDecodeError:
                print 'Error: '
                print full_path.encode('utf8', )

            except Resolver404:
                try:
                    print 'request.get_full_path(): ', request.get_full_path()
                except:
                    pass

                try:
                    print 'Error: Resolver404 - cp1252 [2]', full_path.split('/')[2].encode('cp1252', )
                    print 'Error: Resolver404 - cp1252', full_path.encode('cp1252', )
                except:
                    pass

                try:
                    print 'Error: Resolver404 - utf8 - cp1252', full_path.encode('utf8').encode('cp1252', )
                except:
                    pass

                try:
                    print 'Error: Resolver404 - utf8', full_path.encode('utf8', )
                except:
                    print 'Error: Resolver404 - utf8', 'print value: Error'

            # else:
            #     try:
            #         print 'resolve(full_path, ) : view = ', view, ' args = ', args, ' kwargs = ', kwargs
            #     except:
            #         pass

    #        try:
    #            print 'Not error: ', request.path
    #        except UnicodeEncodeError:
    #            print 'Not print Not error: UniceodeEncodeError'

            if 'view' in locals() and view == show_product:
                print kwargs[u'id'], kwargs[u'product_url'].encode('utf8')
                """ Убираем НАХРЕН проверку именования товара product_url """
                # product = get_product(product_pk=product_pk, product_url=kwargs[u'product_url'], )
                return_dict.update({'canonical': get_product(pk=kwargs[u'id'], ).get_absolute_url(), })
            elif 'view' in locals() and view == show_category:
                print kwargs[u'id'], kwargs[u'category_url'].encode('utf8')
                return_dict.update({'canonical': get_category(pk=kwargs[u'id'], ).get_absolute_url(), })

    sessionid = request.COOKIES.get(u'sessionid', None, )
    if 'kwargs' in locals() and kwargs.get('key'):
        return_dict.update({'viewed': get_or_create_Viewed(request, product_pk=kwargs[u'id'], user_obj=user_object, sessionid=sessionid, ), })
    else:
        return_dict.update({'viewed': None, })

    return_dict.update({'static_pages_': static_pages,
                        'currency_': currency,
                        'current_currency_': current_currency,
                        'slides_': slides,
                        'categories_basement_': categories_basement,
#                        'categories_not_basement_': categories_not_basement,
                        'user_cart_': user_cart,
                        'coupon_': coupon, })
    return return_dict

#    # print type(full_path, )
#    value = None
#    if isinstance(full_path, unicode):
#        try:
#            value = full_path.encode('us-ascii', )
#        except:
#            print 'Not US-ASCII'
#            try:
#                value = full_path.encode('utf8')
#            except:
#                pass
#            else:
#                try:
#                    print 'utf8', type(value, ), value
#                except:
#                    print 'utf8', type(value, ), 'print value: Error'
#            try:
#                value = full_path.decode('cp866').encode('utf8')
#            except:
#                pass
#            else:
#                try:
#                    print 'cp866', type(value, ), value
#                except:
#                    print 'cp866', type(value, ), 'print value: Error'
#            try:
#                value = full_path.decode('cp1251').encode('utf8')
#            except:
#                pass
#            else:
#                try:
#                    print 'cp1251', type(value, ), value
#                except:
#                    print 'cp1251', type(value, ), 'print value: Error'
#            try:
#                value = full_path.decode('cp1252').encode('utf8')
#            except:
#                pass
#            else:
#                try:
#                    print 'cp1252 -1', type(value, ), value
#                except:
#                    print 'cp1252 -1', type(value, ), 'print value: Error'
#            try:
#                value = full_path.encode('cp1252')
#            except:
#                pass
#            else:
#                try:
#                    print 'cp1252 -2', type(value, ), value
#                except:
#                    print 'cp1252 -2', type(value, ), 'print value: Error'
#            #try:
#            #    value = full_path.encode('cp1252').decode('utf8')
#            #except:
#            #    pass
#            #else:
#            #    print 'cp1252 -3', type(value, ), value
#            try:
#                value = full_path.encode('cp1252').encode('utf8')
#            except:
#                pass
#            else:
#                try:
#                    print 'cp1252 -4', type(value, ), value
#                except:
#                    print 'cp1252 -4', type(value, ), 'print value: Error'
#            #try:
#            #    value = full_path.encode('utf8').decode('cp1252').encode('utf8')
#            #except:
#            #    pass
#            #else:
#            #    print 'cp1252 -5', type(value, ), value
#            try:
#                value = full_path.encode('utf8').encode('cp1252')
#            except:
#                pass
#            else:
#                try:
#                    print 'cp1252 -6', type(value, ), value
#                except:
#                    print 'cp1252 -6', type(value, ), 'print value: Error'
#            try:
#                value = full_path.decode('koi8').encode('utf8')
#            except:
#                pass
#            else:
#                try:
#                    print 'koi8', type(value, ), value
#                except:
#                    print 'koi8', type(value, ), 'print value: Error'
#        else:
#            try:
#                print 'ascii', type(value, ), value
#            except:
#                print 'ascii', type(value, ), 'print value: Error'
#
#