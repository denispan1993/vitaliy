# -*- coding: utf-8 -*-
__author__ = 'user'


def ordering_step_one(request,
                      template_name=u'step_one.jinja2.html', ):
    from apps.product.models import Country
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'order_step_one':
            """
                Здесь как-то нужно проверить email
            """
            email = request.POST.get(u'email', False, )
            if email:
                email = email.strip()
            if not email:
                email_error = u'Вы забыли указать Ваш E-Mail.'
            else:
                from proj.settings import SERVER
                from validate_email import validate_email
                email_error = False
                is_valid = True
                if SERVER:
                    is_valid = validate_email(email, check_mx=True, )
                    if not is_valid:
                        # email_error = u'Сервер указанный в Вашем E-Mail - ОТСУТСВУЕТ !!!'
                        email_error = u'Проверьте пожалуйста указанный Вами e-mail.'
                    else:
                        """
                            Если проверка на существование сервера прошла...
                            То делаем полную проверку адреса на существование...
                        """
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
                if is_valid and not email_error:
                    country = request.POST.get(u'select_country', None, )
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
    FIO = request.POST.get(u'FIO', None, )
    phone = request.POST.get(u'phone', None, )
    comment = request.POST.get(u'comment', None, )
    try:
        country_list = Country.objects.all()
    except Country.DoesNotExist:
        country_list = None


def ordering_step_two(request,
                      template_name=u'step_two.jinja2.html', ):
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
                        msg.send(fail_silently=False, )
                        """ Отправка благодарности клиенту. """
                        subject = u'Заказ № %d. Интернет магазин Кексик.' % order.pk
                        html_content = render_to_string('email_suceessful_content.jinja2.html',
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
