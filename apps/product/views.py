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
        basement_categories = Category.manager.basement()
    except Category.DoesNotExist:
        from django.http import Http404
        raise Http404

    return render_to_response(u'category/show_basement_category.jinja2.html',
                              locals(),
                              context_instance=RequestContext(request, ),
                              )


def show_category(request,
                  category_url,
                  id,
                  template_name=u'category/show_category.jinja2.html',
                  ):
    from apps.product.models import Category
    try:
        current_category = Category.objects.get(pk=id, url=category_url, )
    except Category.DoesNotExist:
        current_category = None
        categories_at_current_category = None
        current_products = None
        from django.http import Http404
        raise Http404
    else:
        request.session[u'current_category'] = current_category.pk
        categories_at_current_category_ = current_category.children.all()
        from apps.product.models import Product
        try:
            current_products_ = current_category.products.all()
        except Product.DoesNotExist:
            current_products_ = None

    return render_to_response(u'category/show_category.jinja2.html',
                              locals(),
                              context_instance=RequestContext(request, ),
                              )


def show_product(request, product_url, id,
                 template_name=u'product/show_product.jinja2.html',
                 ):
    current_category = request.session.get(u'current_category', None, )

    if request.method == 'POST':
        if request.session.get(u'cookie', False, ):
        # if cookie:
        # if request.session.test_cookie_worked():
            action = request.POST.get(u'action', None, )
            if action == u'addtocard':
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
                        add_to_cart(request=request,
                                    product=product,
                                    int_product_pk=product_pk,
                                    product_url=product_url,
                                    quantity=quantity_, )
#                        if request.
#                        try:
#                            from apps.cart.models import Cart
#                            cart = Cart.objects.get(sessionid=, )
                    from apps.product.models import Category
                    try:
                        current_category = Category.objects.get(pk=int(current_category, ), )
                    except Category.DoesNotExist:
                        from django.http import Http404
                        raise Http404
                    else:
                        from django.http import HttpResponseRedirect
                        return HttpResponseRedirect(current_category.get_absolute_url(), )
            elif action == u'makeanorder':
                pass
            else:
                from django.http import Http404
                raise Http404
    else:
#        request.session.set_test_cookie()
        from apps.product.models import Product
        try:
            product = Product.objects.get(pk=id, url=product_url, )
        except Product.DoesNotExist:
            from django.http import Http404
            raise Http404
        else:
            product_is_availability = product.is_availability
            categories_of_product = product.category.all()
            if current_category:
                for cat in categories_of_product:
                    if int(current_category) == cat.pk:
                        current_category = categories_of_product[0]
                        break
                else:
                    current_category = categories_of_product[0]
                    request.session[u'current_category'] = current_category.pk
            else:
                current_category = categories_of_product[0]
                request.session[u'current_category'] = current_category.pk
            quantity_ = product.minimal_quantity
            minimal_quantity_ = product.minimal_quantity
            quantity_of_complete_ = product.quantity_of_complete

    return render_to_response(u'product/show_product.jinja2.html',
                              locals(),
                              context_instance=RequestContext(request, ),
                              )


def get_cart(request, ):
    from apps.cart.models import Cart
    if request.user.is_authenticated() and request.user.is_active:
        user_id_ = request.session.get(u'_auth_user_id', None, )
        from django.contrib.auth.models import User
        user_object_ = User.objects.get(pk=user_id_, )
        cart, created = Cart.objects.get_or_create(user=user_object_, sessionid=None, )
    else:
        sessionid = request.COOKIES.get(u'sessionid', None, )
        cart, created = Cart.objects.get_or_create(user=None, sessionid=sessionid, )
    return cart, created


def add_to_cart(request, product=None, int_product_pk=None, product_url=None, quantity=1, ):
#    postdata = request.POST.copy()
    # get product slug from post data, return blank if empty
#    if not product_pk:
#        product_pk = int(postdata.get(u'product_pk', None, ), )
#    if not product_url:
#        product_url = postdata.get(u'product_url', None, )
    if not product:
        # try to get product from cache
        product_cache_key = request.path
        from django.core.cache import cache
        from proj.settings import CACHE_TIMEOUT
        product = cache.get(product_cache_key)
        # if a cache miss, fall back on db query
        if not product:
            # fetch the product or return a missing page error
#            from django.shortcuts import render_to_response, get_object_or_404
#            product = get_object_or_404(Product, pk=product_pk, slug=product_url, )
            from apps.product.models import Product
            try:
                if product_url:
                    product = Product.objects.get(pk=int_product_pk, url=product_url, )
                else:
                    product = Product.objects.get(pk=int_product_pk, )
            except Product.DoesNotExist:
                # request.session[u'test1-product_pk'] = product_pk
                # request.session[u'test1-product_url'] = product_url
                from django.http import Http404
                raise Http404
            else:
                # store item in cache for next time
                cache.set(product_cache_key, product, CACHE_TIMEOUT, )
    # get quantity added, return 1 if empty
#    if not quantity:
#        quantity = int(postdata.get('quantity', 1, ), )
    #get cart
    # Взятие корзины
    product_cart, created = get_cart(request, )
    from apps.cart.models import Product
    try:
        """ Присутсвие конкретного продукта в корзине """
        product_in_cart = product_cart.cart.get(product=product, )
    #        change_exist_cart_option(cart_option=exist_cart_option, quantity=quantity, )
    except Product.DoesNotExist:
        """ Занесение продукта в корзину если его нету """
        product_in_cart = Product.objects.create(key=product_cart,
                                                 product=product,
                                                 price=product.price,
                                                 quantity=quantity, )
        # product_in_cart.update_price_per_piece()
    else:
        product_in_cart.summ_quantity(quantity, )  # quantity += exist_cart_option.quantity
        product_in_cart.update_price_per_piece()
    # finally:
        # product_in_cart.update_price_per_piece()

    return product_cart, product_in_cart
