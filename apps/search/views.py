# -*- coding: utf-8 -*-
from django.db.models import Q
from django.template.loader import get_template
from django.http import HttpResponse

from apps.product.models import Category, Product, ItemID

__author__ = 'AlexStarov'


def search_page(request,
                query,
                template_name=u'category/show_category.jinja2', ):
    categories = None
    products = None
    query = None

    if request.method == 'POST' or request.method == 'GET':

        if 'query' in request.POST and request.POST['query']:
            query = request.POST.get('query', None, )
        elif 'query' in request.GET and request.GET['query']:
            query = request.GET.get('query', None, )

        if query:
            try:
                categories = Category.objects.published(Q(title__icontains=query), )
            except Category.DoesNotExist:
                pass

            try:
                products = Product.objects.published(Q(title__icontains=query), is_availability=1, )
            except Product.DoesNotExist:
                pass

            try:
                ItemsID = ItemID.objects.filter(Q(ItemID__icontains=query, ), )

                for item in ItemsID:
                    try:
                        product = Product.objects.published(ItemID=item, )
                        products = products | product
                    except Product.DoesNotExist:
                        pass

            except ItemID.DoesNotExist:
                pass

    t = get_template(template_name)
    html = t.render(request=request, context={'categories': categories,
                                              'products': products, }, )
    return HttpResponse(html, )
