# coding=utf-8
__author__ = 'Sergey'


def search_page(request,
                query,
                template_name=u'category/show_category.jinja2.html', ):
    if request.method == 'POST':
        if 'query' in request.POST and request.POST['query']:
            query = request.POST.get('query', None, )
            from django.db.models import Q
            from apps.product.models import Category
            try:
                categories = Category.objects.filter(Q(title__icontains=query), )  # | Q(description__icontains=query))
            except Category.DoesNotExist:
                categories = None
            from apps.product.models import Product
            try:
                products = Product.objects.filter(Q(title__icontains=query), )  # | Q(description__icontains=query))
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

            # if products and ItemsID:
            #     products = products + ItemsID
            # elif not products and ItemsID:
            #     products = ItemsID
        else:
            categories = None
            products = None
    else:
        categories = None
        products = None
    from django.template.loader import get_template
    template_name = u'category/show_category.jinja2.html'
    t = get_template(template_name)
    from django.template import RequestContext
    c = RequestContext(request, {'categories': categories,
                                 'products': products, },
                       )
    html = t.render(c)
    from django.http import HttpResponse
    response = HttpResponse(html, )
#    from django.shortcuts import redirect
#    return redirect('/')
    return response
#    from django.shortcuts import render_to_response
#    from django.template import RequestContext
#    return render_to_response(template_name=template_name,
#                              dictionary=locals(),
#                              context_instance=RequestContext(request))
#                              content_type='text/html', )
