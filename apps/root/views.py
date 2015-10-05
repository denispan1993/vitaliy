from django.shortcuts import render_to_response
from django.template import RequestContext


def root_page(request, template_name=u'index.jinja2.html', ):
    if request.method == 'GET':
        GET_NAME = request.GET.get(u'action', False, )
        if GET_NAME == 'delivery':
            id = request.GET.get(u'id', False, )
            url = request.GET.get(u'url', False, )
            if url:
                from django.shortcuts import redirect
                return redirect(to=url, permanent=True, )

    # from apps.product.models import Category
    # try:
    #     categories_basement = Category.objects.basement()
    # except Category.DoesNotExist:
    #     categories_basement = None

    # try:
    #     categories_first = Category.objects.get(pk=1)
    # except Category.DoesNotExist:
    #     categories_first = None

    # from apps.product.models import Product
    # try:
    #     all_products = Product.objects.published()
    # except Product.DoesNotExist:
    #     all_products = None

    # limit_on_page = request.session.get(u'limit_on_page', None, )
    # try:
    #     limit_on_page = int(limit_on_page, )
    # except ValueError:
    #     limit_on_page = 12
    # finally:
    #     in_main_page = Product.manager.in_main_page(limit_on_page, )
    from apps.product.models import Product
    try:
        in_main_page = Product.objects.in_main_page(no_limit=True, )  # limit_on_page, )
    except Product.DoesNotExist:
        in_main_page = None

    # children_categories = categories_first.children.all()

    return render_to_response(template_name=template_name,
                              dictionary={'in_main_page': in_main_page, },
                              # dictionary=locals(),
                              context_instance=RequestContext(request, ),
                              content_type='text/html', )
