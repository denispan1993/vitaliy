# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

# Create your views here.
#from django.conf import settings
#from jinja2 import Environment, FileSystemLoader
#template_dirs = getattr(settings,'TEMPLATE_DIRS', )
#env = Environment(loader=FileSystemLoader(template_dirs, ), )

#default_mimetype = getattr(settings, 'DEFAULT_CONTENT_TYPE', )
#def render_to_response(request, filename, context={}, mimetype=default_mimetype, ):
#    template = env.get_template(filename, )
#    if request:
#        context['request'] = request
#        context['user'] = request.user
#    rendered = template.render(**context)
#    from django.http import HttpResponse
#    return HttpResponse(rendered, mimetype=mimetype, )

#def greater_than_fifty(x, ):
#    return x > 50
#env.tests['gtf'] = greater_than_fifty

from django.shortcuts import render_to_response, render
from django.template import RequestContext, Context
from apps.product.models import Country
from django.shortcuts import redirect


def show_cart(request,
              template_name=u'show_cart.jinja2', ):
#    try:
#        from apps.product.models import Category
#        current_category = Category.objects.get(pk=id, url=category_url, )
#    except Category.DoesNotExist:
#        current_category = None
#        categories_at_current_category = None
#        current_products = None
#        from django.http import Http404
#        raise Http404
#    else:
#        request.session[u'current_category'] = current_category.pk
#        categories_at_current_category_ = current_category.children.all()
#        try:
#            from apps.product.models import Product
#            current_products_ = current_category.products.all()
#        except Product.DoesNotExist:
#            current_products_ = None

    return render(request=request, template_name=template_name, )


def recalc_cart(request, ):
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'recalc_cart':
            # from apps.product.views import get_cart
            """ Взять корзину """
            product_cart, created = get_cart_or_create(request, )
            from apps.cart.models import Product
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
    return redirect(to='show_cart', )


def show_order(request,
               template_name=u'show_order.jinja2', ):
    email = request.POST.get(u'email', False, )
    if email:
        email = email.strip()
    email_error = False
    FIO = request.POST.get(u'FIO', None, )
    phone = request.POST.get(u'phone', None, )
    comment = request.POST.get(u'comment', None, )
    country = request.POST.get(u'select_country', None, )
    try:
        country_list = Country.objects.all()
    except Country.DoesNotExist:
        country_list = None
    delivery_company = request.POST.get(u'select_delivery_company', None, )
    from apps.cart.models import DeliveryCompany
    try:
        delivery_companies_list = DeliveryCompany.objects.all()
    except DeliveryCompany.DoesNotExist:
        delivery_companies_list = None

    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'order':
            """
                Здесь как-то нужно проверить email
            """
            if not email:
                email_error = u'Вы забыли указать Ваш E-Mail.'
            else:
                from proj.settings import SERVER
                from validate_email import validate_email
                is_valid = True
                if SERVER:
                    is_valid = validate_email(email, check_mx=True, )
                    if not is_valid:
                        # email_error = u'Сервер указанный в Вашем E-Mail - ОТСУТСВУЕТ !!!'
                        email_error = u'Проверьте пожалуйста указанный Вами e-mail.'
                    is_valid = validate_email(email, verify=True, )
                if not is_valid:
                    """
                        Делаем повторную проверку на просто валидацию E-Mail адреса
                    """
                    from django.forms import EmailField
                    from django.core.exceptions import ValidationError
                    try:
                        EmailField().clean(email, )
                    except ValidationError:
                        email_error = u'Ваш E-Mail адрес не существует.'
                    else:
                        email_error = False
                        is_valid = True
                if is_valid and not email_error in locals():
                    try:
                        country = int(country, )
                    except (ValueError, TypeError):
                        from django.http import Http404
                        raise Http404
                    else:
                        country = Country.objects.get(pk=country, )
                        """ Взять или создать корзину пользователя """
                        """ Создать теоретически это не нормально """
                        cart, create = get_cart_or_create(request, )
                        if create:
                            return redirect(to=u'/корзина/заказ/непринят/', )
                    from apps.cart.models import Product
                    try:
                        """ Выборка всех продуктов из корзины """
                        all_products = cart.cart.all()
                    except Product.DoesNotExist:
                        """ Странно!!! В корзине нету продуктов!!! """
                        return redirect(to='show_cart', )
                    else:
                        """ Создаем ЗАКАЗ """
                        choice1 = request.POST.get(u'choice1', True, )
                        choice2 = request.POST.get(u'choice2', False, )
                        from apps.cart.models import Order
                        if country.pk == 1:
                            """ для Украины """
                            region = request.POST.get(u'region', None, )
                            settlement = request.POST.get(u'settlement', None, )
                            warehouse_number = request.POST.get(u'warehouse_number', None, )
                            # print type(delivery_company)
                            if delivery_company is None:
                                delivery_company = 1
                            elif type(delivery_company) == unicode:
                                try:
                                    delivery_company = int(delivery_company, )
                                except ValueError:
                                    delivery_company = 1
                            try:
                                delivery_company = DeliveryCompany.objects.get(select_number=delivery_company, )
                            except DeliveryCompany.DoesNotExist:
                                delivery_company = None
                            """ Создаем новый заказ """
                            order = Order.objects.create(user=cart.user,
                                                         sessionid=cart.sessionid,
                                                         email=email,
                                                         FIO=FIO,
                                                         phone=phone,
                                                         country=country,
                                                         delivery_company=delivery_company,
                                                         region=region,
                                                         settlement=settlement,
                                                         warehouse_number=warehouse_number,
                                                         comment=comment,
                                                         checkbox1=choice1,
                                                         checkbox2=choice2, )
                        else:
                            """ для другого Государства """
                            address = request.POST.get(u'address', None, )
                            postcode = request.POST.get(u'postcode', None, )
                            """ Создаем новый заказ """
                            order = Order.objects.create(user=cart.user,
                                                         sessionid=cart.sessionid,
                                                         email=email,
                                                         FIO=FIO,
                                                         phone=phone,
                                                         country=country,
                                                         address=address,
                                                         postcode=postcode,
                                                         comment=comment,
                                                         checkbox1=choice1,
                                                         checkbox2=choice2, )
                        """ Берем указатель на model заказ """
                        from django.contrib.contenttypes.models import ContentType
                        ContentType_Order = ContentType.objects.get_for_model(Order, )
                        """ Перемещение всех продуктов из корзины в заказ """
                        """ Просто меняем 2-а поля назначения у всех продуктов в этой корзине """
                        all_products.update(content_type=ContentType_Order, object_id=order.pk, )
                        """ Удаляем старую корзину """
                        cart.delete()
                        """ Отправка заказа мэнеджеру """
                        subject = u'Заказ № %d. Кексик.' % order.pk
                        from django.template.loader import render_to_string
                        html_content = render_to_string('email_order_content.jinja2.html',
                                                        {'order': order, })
                        from django.utils.html import strip_tags
                        text_content = strip_tags(html_content, )
                        from_email = u'site@keksik.com.ua'
        #                to_email = u'mamager@keksik.com.ua'
        #                from proj.settings import SERVER
        #                if SERVER:
        #                    to_email = u'manager@keksik.com.ua'
        #                else:
        #                    to_email = u'alex.starov@keksik.com.ua'

                        from django.core.mail import get_connection
                        backend = get_connection(backend='django.core.mail.backends.smtp.EmailBackend',
                                                 fail_silently=False, )
                        from django.core.mail import EmailMultiAlternatives
                        from proj.settings import Email_MANAGER
                        msg = EmailMultiAlternatives(subject=subject,
                                                     body=text_content,
                                                     from_email=from_email,
                                                     to=[Email_MANAGER, ],
                                                     connection=backend, )
                        msg.attach_alternative(content=html_content,
                                               mimetype="text/html", )
                        msg.content_subtype = "html"
                        msg.send(fail_silently=False, )
                        """ Отправка благодарности клиенту. """
                        subject = u'Заказ № %d. Интернет магазин Кексик.' % order.pk
                        html_content = render_to_string('email_successful_content.jinja2.html',
                                                        {'order': order, })
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

        #                from django.core.mail import send_mail
        ##                from proj.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_BACKEND
        #                send_mail(subject=subject,
        #                          message='Here is the message.',
        #                          from_email='site@keksik.com.ua',
        #                          recipient_list=['alex.starov@keksik.com.ua', ],
        #                          fail_silently=False,
        #                          connection=backend, )
        ##                          auth_user=EMAIL_HOST_USER,
        ##                          auth_password=EMAIL_HOST_PASSWORD,
        ##                          connection=EMAIL_BACKEND, )
                        request.session[u'order_last'] = order.pk
                        return redirect(to=u'/корзина/заказ/принят/', )
        elif POST_NAME == 'order_cart':
            """ Взять корзину """
            product_cart, created = get_cart_or_create(request, )
            from apps.cart.models import Product
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
    return render_to_response(template_name=template_name,
                              dictionary={'country_list': country_list,
                                          'delivery_companies_list': delivery_companies_list,
                                          'email': email,
                                          'email_error': email_error,
                                          'FIO': FIO,
                                          'phone': phone,
                                          'comment': comment,
                                          'select_country': country,
                                          'select_delivery_company': delivery_company, },
                              context_instance=RequestContext(request, ),
                              content_type='text/html', )


def show_order_success(request,
                       template_name=u'show_order_success.jinja2',
                       ):
    order_pk = request.session.get(u'order_last', None, )
    order = None
    # order_sum = None
    if order_pk is None:
        return redirect(to='show_order_unsuccess', )
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
            # else:
            #     order_sum = order.order_summ()
    return render_to_response(template_name=template_name,
                              dictionary={'order_pk': order_pk,
                                          'order': order,
                                          # 'order_sum': order_sum,
                                          # 'html_text': html_text,
                                          },
                              context_instance=RequestContext(request, ),
                              content_type='text/html', )


def show_order_unsuccess(request,
                         template_name=u'show_order_unsuccess.jinja2',
                         ):
    return render_to_response(template_name=template_name,
                              dictionary={# 'country_list': country_list,
                                          # 'page': page,
                                          # 'html_text': html_text,
                                          },
                              context_instance=RequestContext(request, ),
                              content_type='text/html', )

#def show_product(request,
#                 product_url,
#                 id,
#                 template_name=u'product/show_product.jinja2.html',
#                ):
#    current_category_ = request.session.get(u'current_category', None, )
#
#    if request.method == 'POST':
#        if request.session.test_cookie_worked():
#            action = request.POST.get(u'action', None, )
#            if action == u'addtocard':
#                if current_category_:
#                    product_pk = request.POST.get(u'product_pk', None, )
#                    product_url = request.POST.get(u'product_url', None, )
#                    quantity = request.POST.get(u'quantity', None, )
#                    try:
#                        from apps.product.models import Product
#                        product = Product.objects.get(pk=product_pk, url=product_url, )
#                    except Product.DoesNotExist:
#                        from django.http import Http404
#                        raise Http404
##                    else:
##                        if request.
##                        try:
##                            from apps.cart.models import Cart
##                            cart = Cart.objects.get(sessionid=, )
#                    try:
#                        from apps.product.models import Category
#                        current_category_ = Category.objects.get(pk=int(current_category_, ), )
#                    except Category.DoesNotExist:
#                        from django.http import Http404
#                        raise Http404
#                    else:
#                        from django.http import HttpResponseRedirect
#                        return HttpResponseRedirect(current_category_.get_absolute_url(), )
#            elif action == u'makeanorder':
#                pass
#            else:
#                from django.http import Http404
#                raise Http404
#    else:
##        request.session.set_test_cookie()
#        try:
#            from apps.product.models import Product
#            product_ = Product.objects.get(pk=id, url=product_url, )
#        except Product.DoesNotExist:
#            from django.http import Http404
#            raise Http404
#        else:
#            categories_of_product = product_.category.all()
#            if current_category_:
#                for cat in categories_of_product:
#                    if int(current_category_) == cat.pk:
#                        current_category_ = categories_of_product[0]
#                        break
#                else:
#                    current_category_ = categories_of_product[0]
#                    request.session[u'current_category'] = current_category_.pk
#            else:
#                current_category_ = categories_of_product[0]
#                request.session[u'current_category'] = current_category_.pk
#        quantity_ = 1

#    return render_to_response(u'product/show_product.jinja2.html',
#                              locals(), context_instance=RequestContext(request, ), )


def get_cart_or_create(request, user_object=False, created=True, ):
    sessionid = request.COOKIES.get(u'sessionid', None, )
    # from django.contrib.sessions.models import Session
    # session = Session.objects.get(session_key=request.session.session_key, )
    from apps.cart.models import Cart
    if not user_object:
        if request.user.is_authenticated() and request.user.is_active:
            user_id_ = request.session.get(u'_auth_user_id', None, )
            from django.contrib.auth import get_user_model
            UserModel = get_user_model()
            # from django.contrib.auth.models import User
            try:
                user_id_ = int(user_id_, )
            except ValueError:
                user_object = None
            else:
                user_object = UserModel.objects.get(pk=user_id_, )
        else:
            user_object = None

    if created:
        cart, created = Cart.objects.get_or_create(user=user_object,
                                                   sessionid=sessionid, )
    else:
        try:
            # print user_object
            # print sessionid
            cart = Cart.objects.get(user=user_object,
                                    sessionid=sessionid, )
        except Cart.DoesNotExist:
            cart = None
        return cart

    # print 'Cart:', cart, ' Created:', created
    return cart, created
