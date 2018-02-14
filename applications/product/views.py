# -*- coding: utf-8 -*-
# /apps/product/views.py

# Python 2 and 3:
from __future__ import unicode_literals, print_function
from six import string_types

# Debug
import inspect

from datetime import datetime
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import get_connection, EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags

from applications.cart.order import get_cart_or_create
from applications.utils.datetime2rfc import datetime2rfc
from proj.settings import SERVER, CACHE_TIMEOUT
from .models import Category, Product, Viewed

__author__ = 'AlexStarov'


def debug():
    previous_frame = inspect.currentframe().f_back
    (filename, line_number,
     function_name, lines, index) = inspect.getframeinfo(previous_frame)
    return 'Debug: filename: {filename} | function_name: {function_name} | line number: {line_number}'.\
        format(filename=filename, line_number=line_number, function_name=function_name)


def show_basement_category(request,
                           template_name=u'category/show_basement_category.jinja2', ):
    try:
        basement_categories = Category.objects.basement()
    except Category.DoesNotExist:
        raise Http404

    t = get_template(template_name)
    html = t.render(request=request, context={u'basement_categories': basement_categories, },)
    response = HttpResponse(html, )
    # Мы не можем выяснить когда менялись внутринние подкатегории.
    # Поэтому мы не отдаем дату изменения текущей категории.
    # response['Last-Modified'] = datetime2rfc(current_category.updated_at, )
    return response


def show_category(request,
                  category_url,
                  id,
                  template_name=u'category/show_category.jinja2', ):

    request.session[u'category'] = True
    try:
        current_category = get_category(pk=id)
        # current_category = Category.objects.get(pk=id, url=category_url, )
        request.session[u'current_category'] = current_category.pk

    except Category.DoesNotExist:
        print(debug())
        print('Error: except Category.DoesNotExist: raise Http404')
        raise Http404


#    context_instance = RequestContext(request, )

#    response = render_to_response(template_name=template_name,
#                                  dictionary={'current_category': current_category, },
#                                  context_instance=context_instance,
#                                  content_type='text/html', )
#    return response

    t = get_template(template_name, )

    # c = RequestContext(request, {u'current_category': current_category, }, )

    # html = t.render(c)
    html = t.render(request=request, context={u'current_category': current_category, },)
    response = HttpResponse(html, )

    return response


def show_product(request,
                 product_url,
                 id,
                 template_name=u'product/show_product.jinja2', ):

    current_category = request.session.get(u'current_category', None, )

    request.session[u'product'] = True

    if request.method == 'POST':
        # if request.session.get(u'cookie', False, ):
        # if cookie:
        # if request.session.test_cookie_worked():

        action = request.POST.get(u'action', None, )
        if action == u'addtocard' or action == u'makeanorder':

            product_pk = request.POST.get(u'product_pk', None, )
            product_url = request.POST.get(u'product_url', None, )
            quantity = request.POST.get(u'quantity', None, )

            try:
                product = get_product(pk=id, )
                # product = Product.objects.get(pk=product_pk, url=product_url, )

                add_to_cart(request=request,
                            product=product,
                            int_product_pk=product_pk,
                            quantity=quantity, )

            except Product.DoesNotExist:
                print(debug())
                print('Error: except Product.DoesNotExist: raise Http404')
                raise Http404

            if action == u'makeanorder':
                return redirect(to='cart:show_cart', )

            current_category = get_current_category(current_category=current_category,
                                                    product=product)
            request.session[u'current_category'] = current_category.pk
            return HttpResponseRedirect(current_category.get_absolute_url(), )

        else:
            print(debug())
            print("Error: if action == u'addtocard' or action == u'makeanorder': raise Http404")
            raise Http404
        # else:
        #     raise Http404
    else:
        product = get_product(pk=id, )

        product.get_or_create_ItemID()
        viewed = get_or_create_Viewed(request=request, product=product, )
        # product_is_availability = product.is_availability

        current_category = get_current_category(current_category=current_category, product=product)
        request.session[u'current_category'] = current_category.pk

        quantity_ = product.minimal_quantity
        minimal_quantity_ = product.minimal_quantity
        quantity_of_complete_ = product.quantity_of_complete

    response = render(request=request,
                      template_name=template_name,
                      context=locals(),
                      # context_instance=RequestContext(request, ),
                      content_type='text/html', )
    if SERVER:
        updated_at = product.updated_at
    else:
        updated_at = datetime.now()

    response['Last-Modified'] = datetime2rfc(updated_at, )
    return response


def get_current_category(current_category, product):
    """ Вернуть "текущую" категорию """

    if current_category:
        categories_of_product = product.category.all()

        categories_of_product_pk = [category.pk for category in categories_of_product]

        try:
            current_category = int(current_category)

            if current_category in categories_of_product_pk:
                return categories_of_product.get(pk=current_category)

        except (TypeError, ValueError):
            pass

    """ Ищем главные категории """
    main_category_of_product = product.producttocategory_set.filter(is_main=True)
    # main_category_of_product = categories_of_product.filter(is_main=True)

    if len(main_category_of_product) == 1:
        return main_category_of_product[0].category

    elif len(main_category_of_product) > 1:
        # send_error_manager(product=product, error_id=1, )
        return main_category_of_product[0].category

    elif len(main_category_of_product) == 0:
        # send_error_manager(product=product, error_id=1, )
        print(debug())
        print('Error: if len(main_category_of_product) == 0: product id:', product.pk)

    """ Если не одна из категорий не назнчена главная """
    all_category_of_product = product.producttocategory_set.all()

    if len(all_category_of_product) == 1:
        all_category_of_product[0].is_main = True
        all_category_of_product[0].save()
        return all_category_of_product[0].category

    elif len(all_category_of_product) > 1:
        # send_error_manager(product=product, error_id=1, )
        return all_category_of_product[0].category

    elif len(all_category_of_product) == 0:
        # send_error_manager(product=product, error_id=1, )
        print(debug())
        print('Error: if len(all_category_of_product) == 0: raise Http404: product id:', product.pk)

        raise Http404


def get_category(pk, ):
    if not pk:
        print(debug())
        print('Error: if pk: raise Http404')
        raise Http404

    # Python 2 and 3:
    if isinstance(pk, string_types):
        try:
            pk = int(pk, )
        except (TypeError, ValueError, ):
            print(debug())
            print('Error: except (TypeError, ValueError, ): raise Http404')
            raise Http404

    cache_key = 'cat-%06d' % pk
    cat = cache.get(cache_key, )

    if not cat:
        try:
            cat = Category.objects.get(pk=pk, )
            cache.set(cache_key, cat, CACHE_TIMEOUT, )
        except Category.DoesNotExist:
            print(debug())
            print('Error: except Category.DoesNotExist: raise Http404')
            raise Http404

    return cat


def get_product(pk, ):
    if not pk:
        print(debug())
        print('Error: if pk: raise Http404')
        raise Http404

    # Python 2 and 3:
    if isinstance(pk, string_types):
        try:
            pk = int(pk, )
        except (TypeError, ValueError,):
            print(debug())
            print('Error: except (TypeError, ValueError, ): raise Http404')
            raise Http404

    cache_key = 'prod-%06d' % pk
    prod = cache.get(cache_key, )

    if not prod:
        try:
            prod = Product.objects.get(pk=pk, )
            cache.set(cache_key, prod, CACHE_TIMEOUT, )
        except Product.DoesNotExist:
            print(debug())
            print('Error: except Product.DoesNotExist: raise Http404')
            raise Http404

    return prod


def add_to_cart(request,
                product=None,
                int_product_pk=None,
                quantity=None, ):
    if not product:
        product = get_product(int_product_pk, )

    """ Взятие корзины, или создание если её нету """
    product_cart, created = get_cart_or_create(request, created=True, )
    from applications.cart import models as models_cart
    try:
        """ Присутсвие конкретного продукта в корзине """
        product_in_cart = product_cart.cart.get(product_id=product.pk, )
    except models_cart.Product.DoesNotExist:

        """ Занесение продукта в корзину если его нету """
        if not quantity:
            quantity = product.minimal_quantity  # Минимальное количество заказа

        """ Временная хрень.
            Так как потом возможно нужно будет перейти на количество с дробной частью. """
        try:
            quantity = int(quantity, )
        except ValueError:
            if '.' in quantity:
                quantity = quantity.split('.')[0]
            elif ',' in quantity:
                quantity = quantity.split(',')[0]
            else:
                quantity = 1

            try:
                quantity = int(quantity, )
            except ValueError:
                quantity = 1

        print('key=', product_cart,
              'product=', product,
              'price=', product.price / 2 if product.is_availability == 2 else product.price,
              'percentage_of_prepaid=', 50 if product.is_availability == 2 else 100,
              'quantity=', quantity, )

        product_in_cart = models_cart.Product.objects.create(
            key=product_cart,
            product=product,
            price=product.price / 2 if product.is_availability == 2 else product.price,
            # True - Товар доступен под заказ.
            available_to_order=True if product.is_availability == 2 else False,
            # 50% - предоплата.
            percentage_of_prepaid=50 if product.is_availability == 2 else 100,
            quantity=quantity, )
    else:
        if not quantity:
            quantity = product.quantity_of_complete  # Количество единиц в комплекте
        product_in_cart.sum_quantity(quantity, )  # quantity += exist_cart_option.quantity
        product_in_cart.update_price_per_piece()

    return product_cart, product_in_cart


""" Взять последние просмотренные товары """


def get_or_create_Viewed(request,
                         product=None,
                         product_pk=None,
                         user_obj=None,
                         sessionid=None, ):

    if request.user.is_authenticated()\
            and request.user.is_active\
            and not user_obj:
        user_id_ = request.session.get(u'_auth_user_id', None, )
        user_obj = get_user_model().objects.get(pk=user_id_, )

    if not sessionid:
        sessionid = request.COOKIES.get(u'sessionid', None, )

    if not product and product_pk:
        product = get_product(product_pk, )

    content_type = None
    product_pk = None

    if product:
        content_type = product.content_type
        product_pk = product.pk
        try:
            viewed, created = Viewed.objects.get_or_create(content_type=content_type,
                                                           object_id=product_pk,
                                                           user_obj=user_obj,
                                                           sessionid=sessionid, )
        except MultipleObjectsReturned:
            viewed = Viewed.objects.filter(content_type=content_type,
                                           object_id=product_pk,
                                           user_obj=user_obj,
                                           sessionid=sessionid, )
            viewed.delete()
        else:
            if not created and viewed is not []:
                viewed.last_viewed = timezone.now()
                viewed.save()

    try:
        viewed = Viewed.objects.filter(user_obj=user_obj,
                                       sessionid=sessionid, )\
            .order_by('-last_viewed', )\
            .exclude(content_type=content_type, object_id=product_pk, )

        if len(viewed) > 9:
            viewed[viewed.count() - 1].delete()  # .latest('last_viewed', )

        return viewed

    except Viewed.DoesNotExist:
        return None


def send_error_manager(product=None, error_id=None, ):
    """ Отправка ошибки мэнеджеру """
    subject = u'В товаре № %d ошибка' % product.pk
    html_content = render_to_string('error_email/error_email.jinja2.html',
                                    {'product': product, 'error_id': error_id, })
    text_content = strip_tags(html_content, )
    from_email = u'site@keksik.com.ua'
#                to_email = u'mamager@keksik.com.ua'
    if SERVER:
        to_email = u'manager@keksik.com.ua'
    else:
        to_email = u'alex.starov@keksik.com.ua'

    backend = get_connection(backend='django.core.mail.backends.smtp.EmailBackend',
                             fail_silently=False, )
    msg = EmailMultiAlternatives(subject=subject,
                                 body=text_content,
                                 from_email=from_email,
                                 to=[to_email, ],
                                 connection=backend, )
    msg.attach_alternative(content=html_content,
                           mimetype="text/html", )
    msg.send(fail_silently=False, )
    return None
