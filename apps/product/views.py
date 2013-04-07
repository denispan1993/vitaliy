# Create your views here.
from django.conf import settings
from jinja2 import Environment, FileSystemLoader
template_dirs = getattr(settings, 'TEMPLATE_DIRS', )
env = Environment(loader=FileSystemLoader(template_dirs, ), )

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
        if request.session.test_cookie_worked():
            action = request.POST.get(u'action', None, )
            if action == u'addtocard':
                if current_category:
                    product_pk = request.POST.get(u'product_pk', None, )
                    product_url = request.POST.get(u'product_url', None, )
                    quantity = request.POST.get(u'quantity', None, )
                    from apps.product.models import Product
                    try:
                        product = Product.objects.get(pk=product_pk, url=product_url, )
                    except Product.DoesNotExist:
                        from django.http import Http404
                        raise Http404
#                    else:
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
        quantity_ = 1

    return render_to_response(u'product/show_product.jinja2.html',
                              locals(),
                              context_instance=RequestContext(request, ),
                              )


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
        exist_cart_option.update_quantity(quantity) # quantity += exist_cart_option.quantity
        exist_cart_option.update_price_per_piece()
    #        change_exist_cart_option(cart_option=exist_cart_option, quantity=quantity, )
    except More_Options_Carts.DoesNotExist:
    #        price_per_piece = views_price_per_piece(product, quantity, )
        More_Options_Carts.objects.create(cart=product_cart, price_per_piece=product_cart.product.sale_price(quantity, ), quantity=quantity, color=Color_object, size=Size_object, )
    return None
