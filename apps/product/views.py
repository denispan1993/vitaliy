# coding=utf-8
__author__ = 'Sergey'

# Create your views here.
from django.conf import settings
#from jinja2 import Environment, FileSystemLoader
#template_dirs = getattr(settings, 'TEMPLATE_DIRS', )
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


def show_basement_category(request,
                           template_name=u'category/show_basement_category.jinja2.html',
                           ):
    from apps.product.models import Category
    try:
        basement_categories = Category.objects.basement()
    except Category.DoesNotExist:
        from django.http import Http404
        raise Http404

    from django.template.loader import get_template
    template_name = u'category/show_basement_category.jinja2.html'

    t = get_template(template_name)
    from django.template import RequestContext
    c = RequestContext(request, {u'basement_categories': basement_categories, }, )
#    from django.template import Context
#    c = Context({'basement_categories': basement_categories, }, )
    html = t.render(c)
    from django.http import HttpResponse
    response = HttpResponse(html, )
#    from django.shortcuts import redirect
#    return redirect('/')
    # Мы не можем выяснить когда менялись внутринние подкатегории.
    # Поэтому мы не отдаем дату изменения текущей категории.
##    from apps.utils.datetime2rfc import datetime2rfc
##    response['Last-Modified'] = datetime2rfc(current_category.updated_at, )
    return response

#    return render_to_response(u'category/show_basement_category.jinja2.html',
#                              locals(),
#                              context_instance=RequestContext(request, ),
#                              )


def show_category(request,
                  category_url,
                  id,
                  template_name=u'category/show_content_center.jinja2.html',
                  ):
    request.session[u'category'] = True
    from apps.product.models import Category
    try:
        current_category = Category.objects.get(pk=id, url=category_url, )
    except Category.DoesNotExist:
        current_category = None
        categories_at_current_category_ = None
        current_products_ = None
        from django.http import Http404
        raise Http404
    else:
        request.session[u'current_category'] = current_category.pk
        #categories_at_current_category_ = current_category.children.all()
        #from apps.product.models import Product
        #try:
        #    current_products_ = current_category.products.all()
        #except Product.DoesNotExist:
        #    current_products_ = None

    from django.template.loader import get_template
    template_name = u'category/show_content_center.jinja2.html'
    t = get_template(template_name)
    from django.template import RequestContext
    c = RequestContext(request, {'current_category': current_category, }, )
                                 # 'categories_at_current_category_': categories_at_current_category_,
                                 # 'current_products_': current_products_, }, )
#    from django.template import Context
#    c = Context({'current_category': current_category,
#                 'categories_at_current_category_': categories_at_current_category_,
#                 'current_products_': current_products_, }, )
    html = t.render(c)
    from django.http import HttpResponse
    response = HttpResponse(html, )
#    from django.shortcuts import redirect
#    return redirect('/')
    # Мы не можем выяснить когда менялись внутринние подкатегории.
    # Поэтому мы не отдаем дату изменения текущей категории.
##    from apps.utils.datetime2rfc import datetime2rfc
##    response['Last-Modified'] = datetime2rfc(current_category.updated_at, )
    return response

#    response = render_to_response(
#
#        template_name=u'category/show_content_center.jinja2.html',
#                                  locals(),
##                                  context_instance=RequestContext(request, ),
#                                  )
#    # from datetime import datetime
#    from apps.utils.datetime2rfc import datetime2rfc
#    response['Last-Modified'] = datetime2rfc(current_category.updated_at, )
#    return response


def show_product(request, product_url, id,
                 template_name=u'product/show_product.jinja2.html',
                 ):
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
                    quantity_ = request.POST.get(u'quantity', None, )
                    from apps.product.models import Product
                    try:
                        product = Product.objects.get(pk=product_pk, url=product_url, )
                    except Product.DoesNotExist:
                        # request.session[u'test1-product_pk'] = product_pk
                        # request.session[u'test1-product_url'] = product_url
                        from django.http import Http404
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
                                    quantity=quantity_,
                                    available_to_order=available_to_order, )
#                        if request.
#                        try:
#                            from apps.cart.models import Cart
#                            cart = Cart.objects.get(sessionid=, )
                    if action == u'makeanorder':
                        from django.shortcuts import redirect
                        return redirect(to='show_cart', )
                    from apps.product.models import Category
                    try:
                        current_category = Category.objects.get(pk=int(current_category, ), )
                    except Category.DoesNotExist:
                        from django.http import Http404
                        raise Http404
                    else:
                        from django.http import HttpResponseRedirect
                        return HttpResponseRedirect(current_category.get_absolute_url(), )
#            elif action == u'makeanorder':
#                pass
#            else:
#                from django.http import Http404
#                raise Http404
    else:
#        request.session.set_test_cookie()
        product = get_product(product_pk=id, product_url=product_url, )
#        from apps.product.models import Product
#        try:
#            product = Product.objects.get(pk=id, url=product_url, )
#        except Product.DoesNotExist:
#            from django.http import Http404
#            raise Http404
#        else:
#        products_recommended = product.recommended.all()
        # print(product)
        # print(products_recommended)
        # print(len(products_recommended))
        product.get_or_create_ItemID
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
                        from django.http import Http404
                        raise Http404
                    break
            else:
                    try:
                        current_category = categories_of_product[0]
                    except IndexError:
                        send_error_manager(request, product=product, error_id=1, )
                        from django.http import Http404
                        raise Http404
                    else:
                        request.session[u'current_category'] = current_category.pk
        else:
            current_category = categories_of_product[0]
            request.session[u'current_category'] = current_category.pk
        quantity_ = product.minimal_quantity
        minimal_quantity_ = product.minimal_quantity
        quantity_of_complete_ = product.quantity_of_complete

    response = render_to_response(u'product/show_product.jinja2.html',
                                  locals(),
                                  context_instance=RequestContext(request, ),
                                  )
    from proj.settings import SERVER
    if SERVER:
        updated_at = product.updated_at
    else:
        from datetime import datetime
        updated_at = datetime.now()
    from apps.utils.datetime2rfc import datetime2rfc
    response['Last-Modified'] = datetime2rfc(updated_at, )
    return response


def get_product(product_pk, product_url, ):
#        # try to get product from cache
#        product_cache_key = request.path
#        from django.core.cache import cache
#        from proj.settings import CACHE_TIMEOUT
#        product = cache.get(product_cache_key)
#        # if a cache miss, fall back on db query
    from django.http import Http404
    if type(product_pk, ) is unicode:
        try:
            product_pk = int(product_pk, )
        except ValueError:
            raise Http404
    # product_cache_key = 'product-%.6d' % product_pk
    product_cache_key = 'product-%d' % product_pk
    from django.core.cache import cache
    from proj.settings import CACHE_TIMEOUT
    product = cache.get(product_cache_key, )
    # if a cache miss, fall back on db query
    if not product:
        # fetch the product or return a missing page error
#            from django.shortcuts import render_to_response, get_object_or_404
#            product = get_object_or_404(Product, pk=product_pk, slug=product_url, )
        from apps.product.models import Product
        try:
            if product_url:
                product = Product.objects.get(pk=product_pk, url=product_url, )
            else:
                product = Product.objects.get(pk=product_pk, )
        except Product.DoesNotExist:
            # request.session[u'test1-product_pk'] = product_pk
            # request.session[u'test1-product_url'] = product_url
            raise Http404
        else:
            # store item in cache for next time
            cache.set(product_cache_key, product, CACHE_TIMEOUT, )
    return product


def add_to_cart(request,
                product=None,
                int_product_pk=None,
                product_url=None,
                quantity=None,
                available_to_order=None, ):
#    postdata = request.POST.copy()
    # get product slug from post data, return blank if empty
#    if not product_pk:
#        product_pk = int(postdata.get(u'product_pk', None, ), )
#    if not product_url:
#        product_url = postdata.get(u'product_url', None, )
    if not product:
        product = get_product(int_product_pk, product_url, )
    # get quantity added, return 1 if empty
#    if not quantity:
#        quantity = int(postdata.get('quantity', 1, ), )
    #get cart
    """ Взятие корзины, или создание если её нету """
    from apps.cart.views import get_cart_or_create
    product_cart, created = get_cart_or_create(request, created=True, )
    # print 'Cart created:', created
    from apps.cart.models import Product
    try:
        """ Присутсвие конкретного продукта в корзине """
        product_in_cart = product_cart.cart.get(product=product, )
    #        change_exist_cart_option(cart_option=exist_cart_option, quantity=quantity, )
    except Product.DoesNotExist:
        """ Занесение продукта в корзину если его нету """
        if not quantity:
            quantity = product.minimal_quantity
        if available_to_order is True:
            price = product.price / 2
            percentage_of_prepaid = 50
        else:
            price = product.price
            percentage_of_prepaid = 100
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


#    # Взять последние просмотренные товары
# @property
def get_or_create_Viewed(request,
                         product=None,
                         int_product_pk=None,
                         product_url=None,
                         user_obj=None,
                         sessionid=None, ):
    if not product:
        product = get_product(int_product_pk, product_url, )
    from apps.product.models import Viewed
    if request.user.is_authenticated() and request.user.is_active:
        if not user_obj:
            user_id_ = request.session.get(u'_auth_user_id', None, )
            # from django.contrib.auth.models import User
            from django.contrib.auth import get_user_model
            UserModel = get_user_model()
            user_obj = UserModel.objects.get(pk=user_id_, )
        viewed, created = Viewed.objects.get_or_create(content_type=product.content_type,
                                                       object_id=product.pk,
                                                       user_obj=user_obj,
                                                       sessionid=None, )
    else:
        if not sessionid:
            sessionid = request.COOKIES.get(u'sessionid', None, )
        viewed, created = Viewed.objects.get_or_create(content_type=product.content_type,
                                                       object_id=product.pk,
                                                       user_obj=None,
                                                       sessionid=sessionid, )
    if not created:
        from datetime import datetime
        viewed.last_viewed = datetime.now()
        viewed.save()
    try:
        if request.user.is_authenticated() and request.user.is_active:
            viewed = Viewed.objects.filter(user_obj=user_obj,
                                           sessionid=None, ).order_by('-last_viewed', )
        else:
            viewed = Viewed.objects.filter(user_obj=None,
                                           sessionid=sessionid, ).order_by('-last_viewed', )
    except Viewed.DoesNotExist:
        return None
    else:
        if len(viewed) > 9:
            obj_for_delete = viewed[viewed.count()-1]  # .latest('last_viewed', )
            obj_for_delete.delete()
        return viewed


def send_error_manager(requset=None, product=None, error_id=None, ):
    """ Отправка ошибки мэнеджеру """
    if requset:
        pass
    else:
        pass
    subject = u'В товаре № %d ошибка' % product.pk
    from django.template.loader import render_to_string
    html_content = render_to_string('error_email/error_email.jinja2.html',
                                    {'product': product, 'error_id': error_id, })
    from django.utils.html import strip_tags
    text_content = strip_tags(html_content, )
    from_email = u'site@keksik.com.ua'
#                to_email = u'mamager@keksik.com.ua'
    from proj.settings import SERVER
    if SERVER:
        to_email = u'manager@keksik.com.ua'
    else:
        to_email = u'alex.starov@keksik.com.ua'

    from django.core.mail import get_connection
    backend = get_connection(backend='django.core.mail.backends.smtp.EmailBackend',
                             fail_silently=False, )
    from django.core.mail import EmailMultiAlternatives
    msg = EmailMultiAlternatives(subject=subject,
                                 body=text_content,
                                 from_email=from_email,
                                 to=[to_email, ],
                                 connection=backend, )
    msg.attach_alternative(content=html_content,
                           mimetype="text/html", )
    msg.send(fail_silently=False, )
    return None
