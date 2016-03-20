# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'


def search_page(request,
                query,
                template_name=u'category/show_category.jinja2', ):
    if request.method == 'POST' or request.method == 'GET':

        if 'query' in request.POST and request.POST['query']:
            query = request.POST.get('query', None, )
        elif 'query' in request.GET and request.GET['query']:
            query = request.GET.get('query', None, )

        if ('query' in locals() or 'query' in globals()) and query:
            from django.db.models import Q
            from apps.product.models import Category
            try:
                categories = Category.objects.filter(Q(title__icontains=query), )
            except Category.DoesNotExist:
                categories = None

            from apps.product.models import Product
            try:
                products = Product.objects.filter(Q(title__icontains=query), )
            except Product.DoesNotExist:
                products = None

            from apps.product.models import ItemID
            try:
                ItemsID = ItemID.objects.filter(Q(ItemID__icontains=query, ), )
            except ItemID.DoesNotExist:
                ItemsID = None
            else:
                for item in ItemsID:
                    from apps.product.models import Product
                    try:
                        product = Product.objects.filter(ItemID=item, )
                    except Product.DoesNotExist:
                        pass
                    else:
                        products = products | product
        else:
            categories = None
            products = None
    else:
        categories = None
        products = None

    from django.template.loader import get_template
    t = get_template(template_name)
    html = t.render(request=request, context={'categories': categories,
                                              'products': products, }, )
    from django.http import HttpResponse
    return HttpResponse(html, )
