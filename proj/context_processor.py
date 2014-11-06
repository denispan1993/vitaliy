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
    except Static.DoesNotExist:
        static_pages = None

    from apps.product.models import Currency
    try:
        currency = Currency.objects.all()
    except Currency.DoesNotExist:
        currency = None

    """ Проверяем session на наличие currency pk """
    currency_pk = request.session.get(u'currency_pk', None, )
    if currency_pk:
        try:
            currency_pk = int(currency_pk, )
        except ValueError:
            request.session[u'currency_pk'] = 1
            current_currency = currency.get(pk=1, )
        else:
            try:
                current_currency = currency.get(pk=currency_pk, )
            except Currency.DoesNotExist:
                current_currency = currency.get(pk=1, )
            else:
                request.session[u'currency_pk'] = currency_pk
    else:
        request.session[u'currency_pk'] = 1
        current_currency = currency.get(pk=1, )

    from apps.slide.models import Slide
    try:
        slides = Slide.manager.visible()
        # objects.all().order_by('order', )
    except Slide.DoesNotExist:
        slides = None

    from apps.product.models import Category
    try:
        categories_basement = Category.objects.basement()
    except Category.DoesNotExist:
        categories_basement = None

    if request.user.is_authenticated() and request.user.is_active:
        user_id_ = request.session.get(u'_auth_user_id', None, )
        # from django.contrib.auth.models import User
        from django.contrib.auth import get_user_model
        UserModel = get_user_model()
        try:
            user_id_ = int(user_id_, )
        except ValueError:
            user_object = None
        else:
            user_object = UserModel.objects.get(pk=user_id_, )
    else:
        user_object = None

    from apps.cart.views import get_cart_or_create
    user_cart = get_cart_or_create(request, user_object=user_object, created=False, )

    from django.core.urlresolvers import resolve
    if request.method == 'GET':
        pass
        # view, args, kwargs = resolve(request.path, )
    else:
        """ Оказывается get_full_path() возвращает полный путь со строкой запроса в случае запроса типа GET
            и долбанный resolve не может её тогда обработать и вываливается с кодом 404.
        """
        view, args, kwargs = resolve(request.get_full_path(), )

    from apps.product.views import show_product
    if 'view' in locals() and view == show_product:
        try:
            product_pk = int(kwargs[u'id'], )
        except ValueError:
            pass
        else:
            from apps.product.views import get_product
            product = get_product(product_pk=product_pk, product_url=kwargs[u'product_url'], )
#            from apps.product.models import Product
#            try:
#                product = Product.objects.get(pk=product_pk, url=kwargs[u'product_url'], )
#            except Product.DoesNotExist:
#                product = None
#    else:
#        product = None

    sessionid = request.COOKIES.get(u'sessionid', None, )
    from apps.product.models import Viewed
    if 'product' in locals() and product:
        viewed = Viewed.objects.filter(user_obj=user_object,
                                       sessionid=sessionid, ).\
            order_by('-last_viewed', ).\
            exclude(content_type=product.content_type, object_id=product.pk, )
    else:
        viewed = Viewed.objects.filter(user_obj=user_object,
                                       sessionid=sessionid, ).\
            order_by('-last_viewed', )

    #                    sessionid_carts = Carts.objects.filter(user_obj=None, sessionid=SESSIONID_SESSION_,
    #  order=None, account=None, package=None, ) #cartid=cartid,
    #                except:
    #                    sessionid_carts = None

    #viewed_count = viewed.count()

    return dict(#request=request,
                static_pages_=static_pages,
                currency_=currency,
                current_currency_=current_currency,
                slides_=slides,
                categories_basement_=categories_basement,
                user_cart_=user_cart,
                viewed_=viewed,
                # viewed_count_=viewed_count,
                # view_=view,
                #args_=args,
                #kwargs_=kwargs,
                # product_=product,
                # ajax_resolution_=ajax_resolution_,
                )
