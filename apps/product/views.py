# Create your views here.
#from django.conf import settings
#from jinja2 import Environment, FileSystemLoader
#template_dirs = getattr(settings,'TEMPLATE_DIRS', )
#env = Environment(loader=FileSystemLoader(template_dirs, ), )

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
    try:
        from apps.product.models import Category
        current_category_ = Category.objects.get(pk=id, url=category_url, )
    except Category.DoesNotExist:
        current_category_ = None

    try:
        categories_at_current_category_ = current_category_.children.all()
    except Category.DoesNotExist:
        categories_at_current_category_ = None

    try:
        from apps.product.models import Product
        current_products_ = current_category_.products.all()
    except Product.DoesNotExist:
        current_products_ = None

    return render_to_response(u'category/show_category.jinja2.html',
        locals(),
        context_instance=RequestContext(request, ), )


def show_product(request,
                 product_url,
                 id,
                 template_name=u'product/show_product.jinja2.html',
                ):
    return render_to_response(u'product/show_product.jinja2.html',
        locals(),
        context_instance=RequestContext(request, ), )
