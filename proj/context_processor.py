# coding=utf-8
__author__ = 'Sergey'


def context(request):
#    from apps.product.models import Category
#    try:
#        all_categories_ = Category.manager.published()
#    except Category.DoesNotExist:
#        all_categories_ = None

#    ajax_resolution_ = request.session.get(u'ajax_resolution', True, )
    from apps.static.models import Static
    try:
        static_pages = Static.objects.all()
            #.values_list('order', 'url', 'title', ).order_by('order', )
    except Slide.DoesNotExist:
        static_pages = None

    from apps.product.models import Currency
    try:
        currency = Currency.objects.all()
            #.values_list('order', 'url', 'title', ).order_by('order', )
    except Currency.DoesNotExist:
        currency = None

    from apps.slide.models import Slide
    try:
        slides = Slide.manager.visible()
        # objects.all().order_by('order', )
    except Slide.DoesNotExist:
        slides = None

    from apps.product.models import Category
    try:
        categories_basement = Category.manager.basement()
    except Category.DoesNotExist:
        categories_basement = None

    from apps.cart.models import Cart
    if request.user.is_authenticated() and request.user.is_active:
        user_id_ = request.session.get(u'_auth_user_id', None, )
        if user_id_:
            from django.contrib.auth.models import User
            user_object_ = User.objects.get(pk=user_id_, )
            try:
                user_cart = Cart.objects.get(user=user_object_, sessionid=None, )
            except Cart.DoesNotExist:
                user_cart = None
    else:
        sessionid_COOKIES = request.COOKIES.get(u'sessionid', None, )
        try:
            user_cart = Cart.objects.get(user=None, sessionid=sessionid_COOKIES, )
        except Cart.DoesNotExist:
            user_cart = None

    request_path = request.get_full_path()
    if request_path:
        from django.core.urlresolvers import resolve
        view, args, kwargs = resolve(request.get_full_path(), )

    from apps.product.views import show_product
    if view == show_product:
        from apps.product.models import Product
        try:
            product_pk = int(kwargs[u'id'], )
        except ValueError:
            pass
        else:
            from apps.product.views import get_product
            product = get_product(product_pk=product_pk, product_url=kwargs[u'product_url'], )
#            try:
#                product = Product.objects.get(pk=product_pk, url=kwargs[u'product_url'], )
#            except Product.DoesNotExist:
#                product = None
    else:
        product = None

    from apps.product.models import Viewed
    if request.user.is_authenticated() and request.user.is_active:
        if product:
            viewed = Viewed.objects.filter(user_obj=user_object_,
                                           sessionid=None, ).\
                order_by('-last_viewed', ).\
                exclude(content_type=product.content_type, object_id=product.pk, )
        else:
            viewed = Viewed.objects.filter(user_obj=user_object_,
                                           sessionid=None, ).\
                order_by('-last_viewed', )
    else:
        if product:
            viewed = Viewed.objects.filter(user_obj=None,
                                           sessionid=sessionid_COOKIES, ).\
                order_by('-last_viewed', ).\
                exclude(content_type=product.content_type, object_id=product.pk, )
        else:
            viewed = Viewed.objects.filter(user_obj=None,
                                           sessionid=sessionid_COOKIES, ).\
                order_by('-last_viewed', )
    #                try:
    #                    sessionid_carts = Carts.objects.filter(user_obj=None, sessionid=SESSIONID_SESSION_,
    #  order=None, account=None, package=None, ) #cartid=cartid,
    #                except:
    #                    sessionid_carts = None

    #viewed_count = viewed.count()

    return dict(#request=request,
                static_pages_=static_pages,
                currency_=currency,
                slides_=slides,
                categories_basement_=categories_basement,
                user_cart_=user_cart,
                viewed_=viewed,
                # viewed_count_=viewed_count,
                # view_=view,
                #args_=args,
                #kwargs_=kwargs,
                product_=product,
                # ajax_resolution_=ajax_resolution_,
                )
