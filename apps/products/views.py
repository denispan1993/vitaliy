# Create your views here.
from django.conf import settings
from jinja2 import Environment, FileSystemLoader
template_dirs = getattr(settings,'TEMPLATE_DIRS', )
env = Environment(loader=FileSystemLoader(template_dirs, ), )

default_mimetype = getattr(settings, 'DEFAULT_CONTENT_TYPE', )
def render_to_response(request, filename, context={}, mimetype=default_mimetype, ):
    template = env.get_template(filename, )
    if request:
        context['request'] = request
        context['user'] = request.user
    rendered = template.render(**context)
    from django.http import HttpResponse
    return HttpResponse(rendered, mimetype=mimetype, )

#def greater_than_fifty(x, ):
#    return x > 50
#env.tests['gtf'] = greater_than_fifty

def show_category(request,
                  category_url,
                  id,
                  template_name=u'category/show_category.jinja2.html',
                  ):
    return render_to_response(request, 'category/show_category.jinja2.html', locals(), )


def show_product(request,
                 product_url,
                 id,
                 template_name=u'product/show_product.jinja2.html',
                ):
    return render_to_response(request, 'pruduct/show_product.jinja2.html', locals(), )