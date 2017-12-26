# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve, Resolver404
from django.db.models import QuerySet, Q
from django.core.cache import cache
from django.forms.models import model_to_dict

from applications.cart.order import get_cart_or_create
from applications.product.models import Category, Currency
from applications.product.views import show_category, show_product, get_product, get_category, get_or_create_Viewed
from applications.slide.models import Slide, Recommend
from applications.static.models import Static

__author__ = 'AlexStarov'


def context(request):

    return_dict = {}

    try:
        return_dict.update({'static_pages_': Static.objects.all(), })
    except Static.DoesNotExist:
        return_dict.update({'static_pages_': None, })

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

    currency_dict = cache.get(key='currency_dict_all', )

    if not currency_dict and currency:

        currency_dict = {}
        for currency_inst in currency:
            currency_dict.update({currency_inst.id: model_to_dict(currency_inst)})

        cache.set(
            key='currency_dict_all',
            value=currency_dict,
            timeout=3600, )  # 60 sec * 60 min

    """ Проверяем session на наличие currency pk """
    currency_pk = request.session.get(u'currency_pk', None, )
    try:
        current_currency = currency.get(pk=currency_pk, )
        current_currency_dict = currency_dict.get(int(currency_pk), None, )
    except (Currency.DoesNotExist, ValueError, IndexError):
        current_currency = currency.get(pk=1, )
        current_currency_dict = currency_dict.get(1, None, )
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

    return_dict.update({'slides_': slides, })

    """ Реккомендации """
    recommended = cache.get(key='recommended_visible', )

    if not recommended:
        try:
            recommended = Recommend.objects.all()
            cache.set(
                key='recommended_visible',
                value=recommended,
                timeout=3600, )  # 60 sec * 60 min

        except Recommend.DoesNotExist:
            recommended = None

    return_dict.update({'recommended_': recommended, })

    user_object = None
    if request.user.is_authenticated() and request.user.is_active:
        user_id_ = request.session.get(u'_auth_user_id', None, )
        UserModel = get_user_model()
        try:
            user_id_ = int(user_id_, )
            user_object = UserModel.objects.get(pk=user_id_, )
        except ValueError:
            pass

    user_cart = get_cart_or_create(request, user_object=user_object, created=False, )
    return_dict.update({'user_cart_': user_cart, })

    return_dict.update({'coupon_': None, })
    if user_cart:
        coupons = user_cart.Cart_child.all()
        """ Проверяем СПИСОК [] на пустоту """
        if len(coupons) > 0:
            return_dict.update({'coupon_': coupons[0], })

    #                    sessionid_carts = Carts.objects.filter(user_obj=None, sessionid=SESSIONID_SESSION_,
    #  order=None, account=None, package=None, ) #cartid=cartid,
    #                except:
    #                    sessionid_carts = None

    # #viewed_count = viewed.count()
    # product = None
    # product_pk = None
    # from applications.product.models import Product
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
        print('context_processor.py: 137: ', 'request.method', request.method, )
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
                print('context_processor.py: 153: ', 'resolve:', )
                view, args, kwargs = resolve(full_path, )

            except UnicodeDecodeError:
                print('context_processor.py: 158: ', 'Error: ', )
                print('context_processor.py: 159: ', full_path.encode('utf8', ), )

            except Resolver404:
                try:
                    print('context_processor.py: 163: ', 'request.get_full_path(): ', request.get_full_path(), )
                except:
                    pass

                try:
                    print('context_processor.py: 168: ', 'Error: Resolver404 - cp1252 [2]', full_path.split('/')[2].encode('cp1252', ), )
                    print('context_processor.py: 169: ', 'Error: Resolver404 - cp1252', full_path.encode('cp1252', ), )
                except:
                    pass

                try:
                    print('context_processor.py: 174: ', 'Error: Resolver404 - utf8 - cp1252', full_path.encode('utf8').encode('cp1252', ), )
                except:
                    pass

                try:
                    print('context_processor.py: 179: ', 'Error: Resolver404 - utf8', full_path.encode('utf8', ), )
                except:
                    print('context_processor.py: 181: ', 'Error: Resolver404 - utf8', 'print value: Error', )

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
                print('context_processor.py: 195: ', kwargs[u'id'], kwargs[u'product_url'], )
                """ Убираем НАХРЕН проверку именования товара product_url """
                # product = get_product(product_pk=product_pk, product_url=kwargs[u'product_url'], )
                return_dict.update({'canonical': get_product(pk=kwargs[u'id'], ).get_absolute_url(), })
            elif 'view' in locals() and view == show_category:
                print('context_processor.py: 200: ', kwargs[u'id'], kwargs[u'category_url'], )
                return_dict.update({'canonical': get_category(pk=kwargs[u'id'], ).get_absolute_url(), })

    sessionid = request.COOKIES.get(u'sessionid', None, )
    if 'kwargs' in locals() and kwargs.get('key'):
        return_dict.update({'viewed': get_or_create_Viewed(request, product_pk=kwargs[u'id'], user_obj=user_object, sessionid=sessionid, ), })
    else:
        return_dict.update({'viewed': None, })

    return_dict.update({'basement_top_': get_categories_basement(position=1),
                        'basement_bottom_': get_categories_basement(position=2),
                        })

    return_dict.update({'currency_': currency,
                        'currency_dict_': currency_dict,
                        'current_currency_': current_currency,
                        'current_currency_dict_': current_currency_dict,
                        'basement_': return_dict['basement_top_'] | return_dict['basement_bottom_'],
                        'left_vertical_column_': Category.objects.left_vertical_column(),
                        'footer_column_first_': Category.objects.footer_column_first(),
                        'footer_column_second_': Category.objects.footer_column_second(),
                        'footer_column_third_': Category.objects.footer_column_third(),
                        'footer_column_fourth_': Category.objects.footer_column_fourth(), })
    return return_dict


def get_categories_basement(position: int = 0) -> QuerySet:

    positions = {0: 'basement',
                 1: 'basement_top',
                 2: 'basement_bottom', }

    """ Категории верхнего уровня """
    base = positions[position]
    value = cache.get(key=base, )
    if not value:
        try:
            if position == 0:
                q = Q(location__isnull=False)
            else:
                q = Q(location=position)

            value = Category.objects\
                .basement(q, position=position)\
                .defer('rght', 'mptt_level', 'tree_id', 'template', 'created_at', 'updated_at', )\
                .select_related(
                    'parent',
                    'parent__parent',
                    'parent__parent__parent',
                    'parent__parent__parent__parent',
                    'parent__parent__parent__parent__parent', )
            cache.set(
                key=base,
                value=value,
                timeout=1, )  # 60 sec * 5 min
        except Category.DoesNotExist:
            pass

    return value
