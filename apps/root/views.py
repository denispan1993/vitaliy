from django.shortcuts import render_to_response
from django.template import RequestContext


def root_page(request, template_name=u'index.jinja2.html', ):
    from apps.product.models import Category
    try:
        categories_basement = Category.manager.basement()
    except Category.DoesNotExist:
        categories_basement = None

    try:
        categories_first = Category.objects.get(pk=1)
    except Category.DoesNotExist:
        categories_first = None

    from apps.product.models import Product
    try:
        all_products = Product.manager.published()
    except Product.DoesNotExist:
        all_products = None

    # children_categories = categories_first.children.all()

    return render_to_response(template_name=template_name,
                              dictionary=locals(),
                              context_instance=RequestContext(request, ),
                              content_type='text/html', )
