# coding=utf-8
__author__ = 'Sergey'

from django.shortcuts import render_to_response
#from django.template import RequestContext


def search_page(request,
                query,
                template_name=u'category/show_content_center.jinja2.html', ):
    from django.template import RequestContext
    return render_to_response(template_name=template_name,
                              dictionary=locals(),
                              context_instance=RequestContext(request))
#                              content_type='text/html', )

    if request.method == 'GET':
        if 'query' in request.GET and request.GET['query']:
            err = None
            query = request.GET.get('query', None, )
            from django.db.models import Q
            from apps.product.models import Category
            try:
                categories = Category.objects.filter(Q(title__icontains=query)
                                                     | Q(description__icontains=query))
            except Category.DoesNotExist:
                categories = None
            from apps.product.models import Product
            try:
                products = Product.objects.filter(Q(title__icontains=query)
                                                  | Q(description__icontains=query))
            except Product.DoesNotExist:
                products = None
        else:
            err = None
            categories = None
            products = None
    else:
        err = None
        categories = None
        products = None

#                              dictionary={'err': err,
#                                          'categories': categories,
#                                          'products': products, },


    from django.template.loader import get_template
    template_name = "category/show_content_center.jinja2.html"
    t = get_template(template_name)
    from django.template import Context, RequestContext
    err = 123
    categories = 234
    products = 345
    print('765')
    c = RequestContext(request)
    print('aaa')
    html = t.render(c)
#    html = t.render({'aaa':template_name, })
    print('876')
    from django.http import HttpResponse
    response = HttpResponse(html, )
    from django.shortcuts import redirect
    print('987')
    return redirect('/')
#    return response
