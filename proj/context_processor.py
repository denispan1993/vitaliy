# coding=utf-8
__author__ = 'Sergey'


def context(request):
#    from apps.product.models import Category
#    try:
#        all_categories_ = Category.manager.published()
#    except Category.DoesNotExist:
#        all_categories_ = None

#    ajax_resolution_ = request.session.get(u'ajax_resolution', True, )
    from apps.slide.models import Slide
    try:
        slides = Slide.objects.all().order_by('order', )
    except Slide.DoesNotExist:
        slides = None

    from apps.product.models import Category
    try:
        categories_basement = Category.manager.basement()
    except Category.DoesNotExist:
        categories_basement = None

    from apps.cart.models import Cart
    if request.user.is_authenticated() and request.user.is_active:
        user_id_ = request.session.get('_auth_user_id', None, )
        if user_id_:
            from django.contrib.auth.models import User
            user_object_ = User.objects.get(pk=user_id_, )
            try:
                user_cart = Cart.objects.get(user=user_object_, sessionid=None, )
            except Cart.DoesNotExist:
                user_cart = None
    else:
        sessionid_COOKIES = request.COOKIES.get('sessionid', None, )
        try:
            user_cart = Cart.objects.get(user=None, sessionid=sessionid_COOKIES, )
        except Cart.DoesNotExist:
            user_cart = None

#                try:
#                    sessionid_carts = Carts.objects.filter(user_obj=None, sessionid=SESSIONID_SESSION_, order=None, account=None, package=None, ) #cartid=cartid,
#                except:
#                    sessionid_carts = None

    return dict(request=request,
                slides_=slides,
                categories_basement_=categories_basement,
                user_cart_=user_cart,
                # ajax_resolution_=ajax_resolution_,
                )
