# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import Http404
from django.forms import EmailField
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
import celery
import random
import time

import proj.settings
from applications.product.models import Country
from .tasks import delivery_order, recompile_order
from applications.sms_ussd.tasks import send_template_sms

__author__ = 'AlexStarov'


def ordering_step_one(request,
                      template_name=u'order/step_one.jinja2', ):
    from .models import Product
    try:
        country_list = Country.objects.all()
    except Country.DoesNotExist:
        raise Http404
    FIO = request.session.get(u'FIO', None, )
    email = request.session.get(u'email', None, )
    phone = request.session.get(u'phone', None, )
    select_country = request.session.get(u'select_country', None, )
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'order_cart':
            """ Взять корзину """
            product_cart, create = get_cart_or_create(request, )
            if create:
                return redirect(to=u'/заказ/вы-где-то-оступились/', )
            try:
                """ Выборка всех продуктов из корзины """
                products_in_cart = product_cart.cart.all()
            except Product.DoesNotExist:
                """ Странно!!! В корзине нету продуктов!!! """
                return redirect(to='cart:show_cart', )
            else:
                for product_in_cart in products_in_cart:
                    """ Нужно проверить, есть ли вообще такой продукт в корзине? """
                    product_in_request = request.POST.get(u'product_in_request_%d' % product_in_cart.pk, None, )
                    try:
                        product_in_request = int(product_in_request, )
                    except (ValueError, TypeError, ):
                        continue
                    if product_in_request == product_in_cart.pk:
                        product_del = request.POST.get(u'delete_%d' % product_in_cart.pk, None, )
                        if product_del:
                            product_in_cart.product_delete
                            continue
                        product_quantity = request.POST.get(u'quantity_%d' % product_in_cart.pk, None, )
                        if product_quantity != product_in_cart.quantity:
                            product_in_cart.update_quantity(product_quantity, )
                            continue
                    else:
                        continue
    return render(request=request,
                  template_name=template_name,
                  context={'form_action_next': u'/заказ/второй-шаг/',
                           'FIO': FIO,
                           'email': email,
                           'phone': phone,
                           'country_list': country_list,
                           'select_country': select_country, },
                  content_type='text/html', )


def ordering_step_two(request,
                      template_name=u'order/step_two_ua.jinja2', ):

    from .models import Order, DeliveryCompany

    FIO = request.POST.get(u'FIO', False, )
    if FIO:
        request.session[u'FIO'] = FIO.strip()
    email = request.POST.get(u'email', False, )
    email_error = False
    phone = request.POST.get(u'phone', False, )
    if phone:
        request.session[u'phone'] = phone.strip()
    region, settlement, address, postcode = False, False, False, False
    country = request.POST.get(u'select_country', None, )
    try:
        country_list = Country.objects.all()
    except Country.DoesNotExist:
        raise Http404
    else:
        try:
            select_country = int(country, )
        except (ValueError, TypeError):
            raise Http404
        else:
            country = country_list.get(pk=select_country, )
            if country:
                request.session[u'select_country'] = select_country
            if select_country == 1:
                region = request.session.get(u'region', False, )
                settlement = request.session.get(u'settlement', False, )
            else:
                """ Если страна не Украина """
                template_name = u'order/step_two_others.jinja2'
                address = request.session.get(u'address', False, )
                postcode = request.session.get(u'postcode', False, )
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'ordering_step_one':
            """ Здесь как-то нужно проверить email """
            if email:
                email = email.lower().strip(' ').replace(' ', '', )
                # if SERVER or not SERVER:
                    # if validate_email(email, check_mx=True, ):
                    #    """ Если проверка на существование сервера прошла...
                    #        То делаем полную проверку адреса на существование... """
                    #    is_validate = validate_email(email, verify=True, )
                    # if not is_validate:
                """ Делаем повторную проверку на просто валидацию E-Mail адреса """
                try:
                    EmailField().clean(email, )
                except ValidationError:
                    email_error = u'Ваш E-Mail адрес не существует.'
                # else:
                #     is_validate = True
                # print 'email_error: ', email_error, ' email: ', email
                if not email_error:
                    request.session[u'email'] = email

                    """ Взять или создать корзину пользователя """
                    """ Создать теоретически это не нормально """
                    cart, create = get_cart_or_create(request, )
                    if create:
                        return redirect(to=u'/заказ/вы-где-то-оступились/', )

                    if request.user.is_authenticated() and request.user.is_active:
                        user_id = request.session.get(u'_auth_user_id', None, )
                    sessionid = request.COOKIES.get(u'sessionid', None, )
                    request.session[u'cart_pk'] = cart.pk

                    order_pk = request.session.get(u'order_pk', False, )
                    if order_pk:
                        try:
                            order_pk = int(order_pk, )
                        except ValueError:
                            del order_pk
                    else:
                        del order_pk

                    order_pk_last = request.session.get(u'order_pk_last', False, )
                    if order_pk_last:
                        try:
                            order_pk_last = int(order_pk_last, )
                        except ValueError:
                            del order_pk_last
                    else:
                        del order_pk_last

                    if 'order_pk' in locals()\
                            and 'order_pk_last' in locals()\
                            and order_pk == order_pk_last:
                        del order_pk

                    if 'order_pk' in locals() and order_pk and type(order_pk) == int:
#                        try:
                        q = Q(pk=order_pk,
                              sessionid=sessionid,
                              FIO=FIO,
                              email=email,
                              phone=phone,
                              country_id=select_country, )
                        if request.user.is_authenticated() and request.user.is_active:
    #                                order = Order.objects.get(pk=order_pk,
    #                                                          sessionid=sessionid,
    #                                                          user_id=user_id,
    #                                                          FIO=FIO,
    #                                                          email=email,
    #                                                          phone=phone,
    #                                                          country_id=select_country, )
                            q = q & Q(user_id=user_id, )
    #                            else:
    #                                order = Order.objects.get(pk=order_pk,
    #                                                          sessionid=sessionid,
    #                                                          FIO=FIO,
    #                                                          email=email,
    #                                                          phone=phone,
    #                                                          country_id=select_country, )
                        try:
                            order = Order.objects.get(q)

                        except Order.DoesNotExist:
                            pass

                    if 'order' not in locals():
                        order = Order(sessionid=sessionid, FIO=FIO, email=email,
                                      phone=phone, country_id=select_country, )

                        if request.user.is_authenticated() and request.user.is_active:
                            order.user_id = user_id

                        order.save()

                    request.session[u'order_pk'] = order.pk
                # else:
                #     # email_error = u'Сервер указанный в Вашем E-Mail - ОТСУТСВУЕТ !!!'
                #     email_error = u'Проверьте пожалуйста указанный Вами e-mail.'

            else:
                email_error = u'Вы забыли указать Ваш E-Mail.'
            if email_error:
                template_name = u'order/step_one.jinja2'
        else:
            return redirect(to=u'/заказ/вы-где-то-оступились/', )
    else:
        return redirect(to=u'/заказ/вы-где-то-оступились/', )

    try:
        delivery_companies_list = DeliveryCompany.objects.all()
    except Country.DoesNotExist:
        raise Http404

    return render(request=request,
                  template_name=template_name,
                  context={'form_action_next': u'/заказ/результат-оформления/',
                           'delivery_companies_list': delivery_companies_list,
                           'country_list': country_list,
                           'FIO': FIO,
                           'email': email,
                           'email_error': email_error,
                           'phone': phone,
                           'select_country': country,
                           'region': region,
                           'settlement': settlement,
                           'address': address,
                           'postcode': postcode, },
                  content_type='text/html', )


def result_ordering(request, ):

    from .models import Order, Product

    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'ordering_step_two':

            sessionid = request.COOKIES.get(u'sessionid', None, )
            # print(POST_NAME, sessionid)
            if not cache.get(key='order_%s' % sessionid, ):

                """ Берем случайное значение паузы от 0 до одной секунды для того,
                    что-бы пользователи которые жмут по два раза не успели уйти со страницы. """
                time.sleep(random.uniform(0, 1))

                if not cache.get(key='order_%s' % sessionid, ):
                    cache.set(
                        key='order_%s' % sessionid,
                        value=True,
                        timeout=15, )
                else:
                    return redirect(to='order:already_processing_ru', permanent=True, )

            else:
                return redirect(to='order:already_processing_ru', permanent=True, )

            # FIO = request.session.get(u'FIO', None, )
            # email = request.session.get(u'email', None, )
            # phone = request.session.get(u'phone', None, )
            select_country = request.session.get(u'select_country', None, )

            try:
                order_pk = int(request.session.get(u'order_pk', None, ), )
                try:
                    order = Order.objects.get(pk=order_pk, )

                except Order.DoesNotExist:
                    return redirect(to='order:unsuccessful_ru', permanent=True, )

            except (TypeError, ValueError):
                return redirect(to='order:unsuccessful_ru', permanent=True, )

            if select_country == 1:
                """ Страна Украина """
                region = request.POST.get(u'region', None, )
                order.region = region
                request.session[u'region'] = region
                settlement = request.POST.get(u'settlement', None, )
                order.settlement = settlement
                request.session[u'settlement'] = settlement
                delivery_company = request.POST.get(u'select_delivery_company', None, )
                try:
                    delivery_company = int(delivery_company, )
                except (TypeError, ValueError, ):
                    delivery_company = 1
                # from apps.cart.models import DeliveryCompany
                # try:
                #     delivery_company = DeliveryCompany.objects.get(select_number=delivery_company, )
                # except DeliveryCompany.DoesNotExist:
                #     delivery_company = None
                order.delivery_company_id = delivery_company
                order.warehouse_number = request.POST.get(u'warehouse_number', None, )
                order.checkbox1 = bool(request.POST.get(u'choice1', True, ), )
                order.checkbox2 = bool(request.POST.get(u'choice2', False, ), )
            else:
                """ для любого другого Государства """
                address = request.POST.get(u'address', None, )
                order.address = address
                request.session[u'address'] = address
                postcode = request.POST.get(u'postcode', None, )
                order.postcode = postcode
                request.session[u'postcode'] = postcode

            order.comment = request.POST.get(u'comment', None, )
            order.save()
            cart, create = get_cart_or_create(request, )
            if create:
                return redirect(to='order:unsuccessful_ru', permanent=True, )
            try:
                """ Выборка всех продуктов из корзины """
                all_products = cart.cart.all()
            except Product.DoesNotExist:
                """ Странно!!! В корзине нету продуктов!!! """
                return redirect(to='cart:show_cart', )
            else:
                """ Берем указатель на model заказ """
                ContentType_Order = ContentType.objects.get_for_model(Order, )
                """ Перемещение всех продуктов из корзины в заказ """
                """ Просто меняем 2-а поля назначения у всех продуктов в этой корзине """
                all_products.update(content_type=ContentType_Order, object_id=order.pk, )

                """ Переносим ссылающийся купон с "корзины" на "заказ" """
                coupons = cart.Cart_child.all()
                if len(coupons) == 1:
                    """ Удаляем ссылку на "корзину" """
                    coupons[0].child_cart.remove(cart, )
                    """ Добавляем ссылку на "заказ" """
                    coupons[0].child_order.add(order, )
                    print('Coupon_key: ', coupons[0].key)

                """ Удаляем старую корзину """
                cart.delete()

                """ Отправляем менеджеру заказ с описанием
                    а пользователя благодарное письмо номером заказа и предварительной суммой
                    и просьбой подождать звонка менеджера для уточнения заказа """
                delivery_order.apply_async(
                    queue='delivery_send',
                    kwargs={'order_pk': order.pk,
                            'email_template_name_to_admin': proj.settings.EMAIL_TEMPLATE_NAME['SEND_ORDER_TO_ADMIN'],
                            'email_template_name_to_client': proj.settings.EMAIL_TEMPLATE_NAME['SEND_ORDER_NUMBER'], },
                    task_id='celery-task-id-delivery_order-{0}'.format(celery.utils.uuid(), ),
                )

                phone = order.phone.lstrip('+').replace('(', '').replace(')', '')\
                    .replace(' ', '').replace('-', '').replace('.', '').replace(',', '') \
                    .lstrip('380').lstrip('38').lstrip('80').lstrip('0')

                if len(phone, ) == 9:
                    send_template_sms.apply_async(
                        queue='delivery_send',
                        kwargs={
                            'sms_to_phone_char': '+380%s' % phone[:9],
                            'sms_template_name': proj.settings.SMS_TEMPLATE_NAME['SEND_ORDER_NUMBER'],
                            'sms_order_number': order.number,
                        },
                        task_id='celery-task-id-send_template_sms-{0}'.format(celery.utils.uuid(), ),
                    )

                request.session[u'order_pk_last'] = order.pk

                recompile_order.apply_async(
                    queue='celery',
                    kwargs={'order_pk': order.pk, },
                    task_id='celery-task-id-recompile_order-{0}'.format(celery.utils.uuid(), ),
                )

                return redirect(to='order:successful_ru', permanent=True, )
        else:
            return redirect(to='order:unsuccessful_ru', permanent=True, )
    else:
        return redirect(to='order:unsuccessful_ru', permanent=True, )


def order_success(request,
                  template_name=u'order/successful.jinja2', ):

    from .models import Order

    order_pk = request.session.get(u'order_pk_last', None, )
    order = None

    if order_pk is None:
        return redirect(to='order:unsuccessful_ru', )

    else:
        try:
            order_pk = int(order_pk, )
            try:
                order = Order.objects.get(pk=order_pk, )
            except Order.DoesNotExist:
                order_pk = None; order = None
        except ValueError:
            order_pk = None; order = None

    return render(request=request,
                  template_name=template_name,
                  context={'order_pk': order_pk,
                           'order': order, },
                  content_type='text/html', )


def get_cart_or_create(request, user_object=False, created=True, ):

    from .models import Cart

    sessionid = request.COOKIES.get(u'sessionid', None, )

    if not user_object:
        if request.user.is_authenticated() and request.user.is_active:
            user_id_ = request.session.get(u'_auth_user_id', None, )

            try:
                user_id_ = int(user_id_, )
                user_object = get_user_model().objects.get(pk=user_id_, )

            except ValueError:
                user_object = None
        else:
            user_object = None

    if created:
        cart, created = Cart.objects.get_or_create(user=user_object,
                                                   sessionid=sessionid, )
    else:
        try:
            cart = Cart.objects.get(user=user_object,
                                    sessionid=sessionid, )
        except Cart.DoesNotExist:
            cart = None
        return cart

    return cart, created
