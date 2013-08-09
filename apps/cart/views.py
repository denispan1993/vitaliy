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
            from apps.product.views import get_cart
            """ Взять корзину """
            product_cart, created = get_cart(request, )
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
               template_name=u'show_order.jinja2.html',
               ):
    from apps.product.models import Country
    try:
        country_list = Country.objects.all()
    except Country.DoesNotExist:
        country_list = None
    # return render_to_response(u'show_order.jinja2.html', locals(), context_instance=RequestContext(request, ), )
    return render_to_response(template_name=template_name,
                              dictionary={ 'country_list': country_list,
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


def get_cart(request, ):
    if request.user.is_authenticated() and request.user.is_active:
        user_id_ = request.session.get(u'_auth_user_id', None, )
        from django.contrib.auth.models import User
        user_object_ = User.objects.get(pk=user_id_)
        from apps.cart.models import Cart
        cart, created = Cart.objects.get_or_create(user=user_object_, sessionid=None, )
    else:
        sessionid = request.COOKIES.get(u'sessionid', None, )
        cart, created = Cart.objects.get_or_create(user=None, sessionid=sessionid, )
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
    product_cart = get_cart(request, )
    try:
        exist_cart_option = product_cart.cart.get(color=Color_object, size=Size_object, )
        exist_cart_option.summ_quantity(quantity) # quantity += exist_cart_option.quantity
        exist_cart_option.update_price_per_piece()
    #        change_exist_cart_option(cart_option=exist_cart_option, quantity=quantity, )
    except More_Options_Carts.DoesNotExist:
    #        price_per_piece = views_price_per_piece(product, quantity, )
        More_Options_Carts.objects.create(cart=product_cart, price_per_piece=product_cart.product.sale_price(quantity, ), quantity=quantity, color=Color_object, size=Size_object, )
    return None
