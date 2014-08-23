# coding=utf-8
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

from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.product.models import Country


def show_cart(request,
              template_name=u'show_cart.jinja2.html',
              ):
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

    return render_to_response(u'show_cart.jinja2.html',
                              locals(),
                              context_instance=RequestContext(request, ), )


def recalc_cart(request, ):
    from django.shortcuts import redirect
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
                    except ValueError:
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
               template_name=u'show_order.jinja2.html', ):
    try:
        country_list = Country.objects.all()
    except Country.DoesNotExist:
        country_list = None
    if request.method == 'POST':
        POST_NAME = request.POST.get(u'POST_NAME', None, )
        if POST_NAME == 'order':
            email = request.POST.get(u'email', None, )
            FIO = request.POST.get(u'FIO', None, )
            phone = request.POST.get(u'phone', None, )
            comment = request.POST.get(u'comment', None, )
            country = request.POST.get(u'select_country', None, )
            try:
                country = int(country)
            except ValueError:
                from django.http import Http404
                raise Http404
            else:
                country = Country.objects.get(pk=country, )
                """ Взять или создать корзину пользователя """
                """ Создать теоретически это не нормально """
                cart, create = get_cart_or_create(request, )
            from apps.cart.models import Product
            try:
                """ Выборка всех продуктов из корзины """
                all_products = cart.cart.all()
            except Product.DoesNotExist:
                """ Странно!!! В корзине нету продуктов!!! """
                return redirect(to='show_cart', )
            else:
                """ Создаем ЗАКАЗ """
                from apps.cart.models import Order
                if country.pk == 1:
                    """ для Украины """
                    region = request.POST.get(u'region', None, )
                    settlement = request.POST.get(u'settlement', None, )
                    warehouse_number = request.POST.get(u'warehouse_number', None, )
                    """ Создаем новый заказ """
                    order = Order.objects.create(user=cart.user,
                                                 sessionid=cart.sessionid,
                                                 email=email,
                                                 FIO=FIO,
                                                 phone=phone,
                                                 country=country,
                                                 region=region,
                                                 settlement=settlement,
                                                 warehouse_number=warehouse_number,
                                                 comment=comment, )
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
                                                 comment=comment, )
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
                subject = u'Заказ № %d. Интернет магазин Кексик.'
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
                from django.shortcuts import redirect
                return redirect(to=u'/корзина/заказ/принят/', )
    return render_to_response(template_name=template_name,
                              dictionary={'country_list': country_list, },
                              context_instance=RequestContext(request, ),
                              content_type='text/html', )


def show_order_success(request,
                       template_name=u'show_order_success.jinja2.html',
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


def add_to_cart(request):
    postdata = request.POST.copy()
    # get product slug from post data, return blank if empty
    product_pk = int(postdata.get(u'product_pk', None, ), )
    product_url = postdata.get(u'product_url', None, )
    product_cache_key = request.path
    # try to get product from cache
    from django.core.cache import cache
    from proj.settings import CACHE_TIMEOUT
    product = cache.get(product_cache_key)
    # if a cache miss, fall back on db query
    if not product:
        # fetch the product or return a missing page error
        from django.shortcuts import render_to_response, get_object_or_404
        from apps.product.models import Product
        product = get_object_or_404(Product, pk=product_pk, slug=product_url, )
        # store item in cache for next time
        cache.set(product_cache_key, product, CACHE_TIMEOUT)
        # get quantity added, return 1 if empty
    quantity = int(postdata.get('quantity', 1, ), )
    #get cart
    product_cart = get_cart_or_create(request, )
    try:
        exist_cart_option = product_cart.cart.get(color=Color_object, size=Size_object, )
        exist_cart_option.summ_quantity(quantity) # quantity += exist_cart_option.quantity
        exist_cart_option.update_price_per_piece()
    #        change_exist_cart_option(cart_option=exist_cart_option, quantity=quantity, )
    except More_Options_Carts.DoesNotExist:
    #        price_per_piece = views_price_per_piece(product, quantity, )
        More_Options_Carts.objects.create(cart=product_cart, price_per_piece=product_cart.product.sale_price(quantity, ), quantity=quantity, color=Color_object, size=Size_object, )
    return None
