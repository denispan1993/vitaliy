# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
import celery

from proj.settings import SERVER
from apps.product.models import Country
from .tasks import delivery_order
from .models import Order, Product, DeliveryCompany
from .views import get_cart_or_create

__author__ = 'AlexStarov'


def ordering_step_one(request,
                      template_name=u'order/step_one.jinja2', ):
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
                return redirect(to='show_cart', )
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
                email = email.strip()
                if SERVER or not SERVER:
                    # if validate_email(email, check_mx=True, ):
                    #    """ Если проверка на существование сервера прошла...
                    #        То делаем полную проверку адреса на существование... """
                    #    is_validate = validate_email(email, verify=True, )
                    # if not is_validate:
                    """ Делаем повторную проверку на просто валидацию E-Mail адреса """
                    from django.forms import EmailField
                    from django.core.exceptions import ValidationError
                    try:
                        EmailField().clean(email, )
                    except ValidationError:
                        email_error = u'Ваш E-Mail адрес не существует.'
                    # else:
                    #     is_validate = True
                    print 'email_error: ', email_error, ' email: ', email
                    if not email_error:
                        request.session[u'email'] = email
                        """ Взять или создать корзину пользователя """
                        """ Создать теоретически это не нормально """
                        from apps.cart.views import get_cart_or_create
                        cart, create = get_cart_or_create(request, )
                        if create:
                            return redirect(to=u'/заказ/вы-где-то-оступились/', )
                        if request.user.is_authenticated() and request.user.is_active:
                            user_id = request.session.get(u'_auth_user_id', None, )
                        sessionid = request.COOKIES.get(u'sessionid', None, )
                        request.session[u'cart_pk'] = cart.pk
                        order_pk = request.session.get(u'order_pk', False, )
                        order_pk_last = request.session.get(u'order_pk_last', False, )
                        if order_pk:
                            try:
                                order_pk = int(order_pk, )
                            except ValueError:
                                del order_pk
                        else:
                            del order_pk
                        if order_pk_last:
                            try:
                                order_pk_last = int(order_pk_last, )
                            except ValueError:
                                del order_pk_last
                        else:
                            del order_pk_last
                        if 'order_pk' in locals() or 'order_pk' in globals():
                            if 'order_pk_last' in locals() or 'order_pk_last' in globals():
                                if order_pk == order_pk_last:
                                    del order_pk
                        from apps.cart.models import Order
                        if ('order_pk' in locals() or 'order_pk' in globals()) and order_pk and type(order_pk) == int:
                            try:
                                if request.user.is_authenticated() and request.user.is_active:
                                    order = Order.objects.get(pk=order_pk,
                                                              sessionid=sessionid,
                                                              user_id=user_id,
                                                              FIO=FIO,
                                                              email=email,
                                                              phone=phone,
                                                              country_id=select_country, )
                                else:
                                    order = Order.objects.get(pk=order_pk,
                                                              sessionid=sessionid,
                                                              FIO=FIO,
                                                              email=email,
                                                              phone=phone,
                                                              country_id=select_country, )
                            except Order.DoesNotExist:
                                pass
                        if 'order' not in locals() and 'order' not in globals():
                            order = Order()
                            order.sessionid = sessionid
                            if request.user.is_authenticated() and request.user.is_active:
                                order.user_id = user_id
                            order.FIO = FIO
                            order.email = email
                            order.phone = phone
                            order.country_id = select_country
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
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'ordering_step_two':
            FIO = request.session.get(u'FIO', None, )
            email = request.session.get(u'email', None, )
            phone = request.session.get(u'phone', None, )
            select_country = request.session.get(u'select_country', None, )
            order_pk = request.session.get(u'order_pk', None, )
            try:
                order_pk = int(order_pk, )
            except ValueError:
                return redirect(to=u'/заказ/вы-где-то-оступились/', )

            try:
                order = Order.objects.get(pk=order_pk, )
            except Order.DoesNotExist:
                return redirect(to=u'/заказ/вы-где-то-оступились/', )
            if select_country == 1:
                """ Страна Украина """
                region = request.POST.get(u'region', None, )
                order.region = region
                request.session[u'region'] = region
                settlement = request.POST.get(u'settlement', None, )
                order.settlement = settlement
                request.session[u'settlement'] = settlement
                delivery_company = request.POST.get(u'select_delivery_company', None, )
                if delivery_company is None:
                    delivery_company = 1
                elif type(delivery_company) == unicode:
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
                warehouse_number = request.POST.get(u'warehouse_number', None, )
                order.warehouse_number = warehouse_number
                choice1 = request.POST.get(u'choice1', True, )
                order.checkbox1 = choice1
                choice2 = request.POST.get(u'choice2', False, )
                order.checkbox2 = choice2
            else:
                """ для любого другого Государства """
                address = request.POST.get(u'address', None, )
                order.address = address
                request.session[u'address'] = address
                postcode = request.POST.get(u'postcode', None, )
                order.postcode = postcode
                request.session[u'postcode'] = postcode
            comment = request.POST.get(u'comment', None, )
            order.comment = comment
            order.save()
            cart, create = get_cart_or_create(request, )
            if create:
                return redirect(to=u'/заказ/вы-где-то-оступились/', )
            try:
                """ Выборка всех продуктов из корзины """
                all_products = cart.cart.all()
            except Product.DoesNotExist:
                """ Странно!!! В корзине нету продуктов!!! """
                return redirect(to='show_cart', )
            else:
                """ Берем указатель на model заказ """
                ContentType_Order = ContentType.objects.get_for_model(Order, )
                """ Перемещение всех продуктов из корзины в заказ """
                """ Просто меняем 2-а поля назначения у всех продуктов в этой корзине """
                all_products.update(content_type=ContentType_Order, object_id=order.pk, )
                """ Удаляем старую корзину """
                cart.delete()

                delivery = delivery_order.apply_async(
                    queue='delivery_send',
                    kwargs={'order_pk': order.pk, },
                    task_id='celery-task-id-{0}'.format(celery.utils.uuid(), ),
                )

                request.session[u'order_pk_last'] = order.pk

                return redirect(to=u'/заказ/оформление-прошло-успешно/', )
        else:
            return redirect(to=u'/заказ/вы-где-то-оступились/', )
    else:
        return redirect(to=u'/заказ/вы-где-то-оступились/', )


def order_success(request,
                  template_name=u'order/success.jinja2', ):
    order_pk = request.session.get(u'order_pk_last', None, )
    order = None
    if order_pk is None:
        return redirect(to='cart:order_unsuccessful_ru', )
    else:
        try:
            order_pk = int(order_pk, )
        except ValueError:
            order_pk = None
        else:
            from apps.cart.models import Order
            try:
                order = Order.objects.get(pk=order_pk, )
            except Order.DoesNotExist:
                pass
    return render(request=request,
                  template_name=template_name,
                  context={'order_pk': order_pk,
                           'order': order, },
                  content_type='text/html', )


def order_unsuccessful(request,
                       template_name=u'show_order_unsuccess.jinja2', ):
    return render(request=request,
                  template_name=template_name,
                  content_type='text/html', )


def aaa():
    """ Отправка заказа мэнеджеру """
    subject = u'Заказ № %d. Интернет магазин Кексик.' % order.pk
    html_content = render_to_string('email_order_content.jinja2',
                                    {'order': order, })
    text_content = strip_tags(html_content, )
    from_email = u'site@keksik.com.ua'
    #                to_email = u'mamager@keksik.com.ua'
    #                from proj.settings import SERVER
    #                if SERVER:
    #                    to_email = u'manager@keksik.com.ua'
    #                else:
    #                    to_email = u'alex.starov@keksik.com.ua'

    backend = get_connection(backend='django.core.mail.backends.smtp.EmailBackend',
                             fail_silently=False, )
    msg = EmailMultiAlternatives(subject=subject,
                                 body=text_content,
                                 from_email=from_email,
                                 to=['zakaz@keksik.com.ua', ],
                                 connection=backend, )
    msg.attach_alternative(content=html_content,
                           mimetype="text/html", )
    msg.send(fail_silently=False, )
    """ Отправка благодарности клиенту. """
    subject = u'Заказ № %d. Интернет магазин Кексик.' % order.pk
    html_content = render_to_string('email_successful_content.jinja2',
                                    {'order': order, }, )
    text_content = strip_tags(html_content, )
    from_email = u'site@keksik.com.ua'
    to_email = email
    msg = EmailMultiAlternatives(subject=subject,
                                 body=text_content,
                                 from_email=from_email,
                                 to=[to_email, ],
                                 connection=backend, )
    msg.attach_alternative(content=html_content,
                           mimetype="text/html", )
    msg.send(fail_silently=False, )
