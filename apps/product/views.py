# -*- coding: utf-8 -*-

from datetime import datetime
from django.template import RequestContext
from django.template.loader import get_template, render_to_string
from apps.utils.datetime2rfc import datetime2rfc
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.cache import cache
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import get_connection, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model

from proj.settings import SERVER, CACHE_TIMEOUT

from apps.cart import models as models_cart
from apps.cart.views import get_cart_or_create
from .models import Category, Product, Viewed

__author__ = 'AlexStarov'


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
        current_category = Category.objects.get(pk=id, url=category_url, )
    except Category.DoesNotExist:
        current_category = None
        categories_at_current_category_ = None
        current_products_ = None
        raise Http404
    else:
        request.session[u'current_category'] = current_category.pk
        #categories_at_current_category_ = current_category.children.all()
        #try:
        #    current_products_ = current_category.products.all()
        #except Product.DoesNotExist:
        #    current_products_ = None


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
        if request.session.get(u'cookie', False, ):
        # if cookie:
        # if request.session.test_cookie_worked():
            action = request.POST.get(u'action', None, )
            if action == u'addtocard' or action == u'makeanorder':
                if current_category:
                    product_pk = request.POST.get(u'product_pk', None, )
                    product_url = request.POST.get(u'product_url', None, )
                    quantity = request.POST.get(u'quantity', None, )
                    try:
                        product = Product.objects.get(pk=product_pk, )
                        # product = Product.objects.get(pk=product_pk, url=product_url, )
                    except Product.DoesNotExist:
                        raise Http404
                    else:
                        if product.is_availability == 2:
                            available_to_order = True
                        else:
                            available_to_order = False
                        add_to_cart(request=request,
                                    product=product,
                                    int_product_pk=product_pk,
                                    product_url=product_url,
                                    quantity=quantity,
                                    available_to_order=available_to_order, )
#                        if request.
#                        try:
#                            cart = Cart.objects.get(sessionid=, )
                    if action == u'makeanorder':
                        return redirect(to='show_cart', )
                    try:
                        current_category = Category.objects.get(pk=int(current_category, ), )
                    except Category.DoesNotExist:
                        raise Http404
                    else:
                        return HttpResponseRedirect(current_category.get_absolute_url(), )
#            elif action == u'makeanorder':
#                pass
                else:
                    raise Http404
            else:
                raise Http404
        else:
            raise Http404
    else:
        product = get_product(product_pk=id, product_url=product_url, )

        product.get_or_create_ItemID()
        viewed = get_or_create_Viewed(request=request, product=product, )
        # product_is_availability = product.is_availability
        categories_of_product = product.category.all()
        if current_category:
            for cat in categories_of_product:
                if int(current_category) == cat.pk:
                    try:
                        current_category = categories_of_product[0]
                    except IndexError:
                        send_error_manager(request, product=product, error_id=1, )
                        raise Http404
                    break
            else:
                try:
                    current_category = categories_of_product[0]
                except IndexError:
                    send_error_manager(request, product=product, error_id=1, )
                    raise Http404
                else:
                    request.session[u'current_category'] = current_category.pk
        else:
            current_category = categories_of_product[0]
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


def get_product(product_pk, product_url=None, ):
    if type(product_pk, ) is unicode:
        try:
            product_pk = int(product_pk, )
        except ValueError:
            raise Http404
    product_cache_key = 'product-%d' % product_pk
    product = cache.get(product_cache_key, )
    if not product:
        # fetch the product or return a missing page error
#            product = get_object_or_404(Product, pk=product_pk, slug=product_url, )
        try:
            #if product_url:
            """ Задумываюсь о необходимости проверки URL """
            """ Уже не задумываюсь """
            #    print 'Product_pk: ', product_pk, ' product_url: ', product_url
            #    product = Product.objects.get(pk=product_pk, url=product_url, )
            #else:
            #    product = Product.objects.get(pk=product_pk, )
            product = Product.objects.get(pk=product_pk, )
        except Product.DoesNotExist:
            raise Http404
        else:
            cache.set(product_cache_key, product, CACHE_TIMEOUT, )
    return product


def add_to_cart(request,
                product=None,
                int_product_pk=None,
                product_url=None,
                quantity=None,
                available_to_order=None, ):
    if not product:
        product = get_product(int_product_pk, product_url, )
    """ Взятие корзины, или создание если её нету """
    product_cart, created = get_cart_or_create(request, created=True, )
    try:
        """ Присутсвие конкретного продукта в корзине """
        product_in_cart = product_cart.cart.get(product=product, )
    except models_cart.Product.DoesNotExist:
        """ Занесение продукта в корзину если его нету """
        if not quantity:
            quantity = product.minimal_quantity
        if available_to_order is None:
            available_to_order = product.is_availability == 2
        if available_to_order is True:
            price = product.price / 2
            percentage_of_prepaid = 50
        else:
            price = product.price
            percentage_of_prepaid = 100
        """ Временная хрень.
         Так как потом возможно нужно будет перейти на количество с дробной частью.
        """
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

        product_in_cart = Product.objects.create(key=product_cart,
                                                 product=product,
                                                 price=price,
                                                 # True - Товар доступен под заказ.
                                                 available_to_order=available_to_order,
                                                 # 50% - предоплата.
                                                 percentage_of_prepaid=percentage_of_prepaid,
                                                 quantity=quantity, )
    else:
        if not quantity:
            quantity = product.quantity_of_complete
        product_in_cart.summ_quantity(quantity, )  # quantity += exist_cart_option.quantity
        product_in_cart.update_price_per_piece()
    # finally:
        # product_in_cart.update_price_per_piece()

    return product_cart, product_in_cart


""" Взять последние просмотренные товары """


def get_or_create_Viewed(request,
                         product=None,
                         int_product_pk=None,
                         product_url=None,
                         user_obj=None,
                         sessionid=None, ):
    if not product and int_product_pk and product_url:
        product = get_product(int_product_pk, product_url, )

    if request.user.is_authenticated() and request.user.is_active:
        if not user_obj:
            user_id_ = request.session.get(u'_auth_user_id', None, )
            UserModel = get_user_model()
            user_obj = UserModel.objects.get(pk=user_id_, )
    else:
        if not sessionid:
            sessionid = request.COOKIES.get(u'sessionid', None, )

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
                viewed.last_viewed = datetime.now()
                viewed.save()
    else:
        content_type = None
        product_pk = None

    try:
        viewed = Viewed.objects.filter(user_obj=user_obj,
                                       sessionid=sessionid, )\
            .order_by('-last_viewed', )\
            .exclude(content_type=content_type, object_id=product_pk, )
    except Viewed.DoesNotExist:
        return None
    else:
        if len(viewed) > 9:
            obj_for_delete = viewed[viewed.count()-1]  # .latest('last_viewed', )
            obj_for_delete.delete()
        return viewed


def send_error_manager(requset=None, product=None, error_id=None, ):
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
