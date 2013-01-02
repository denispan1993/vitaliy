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

def root(request, template_name='root.jinja2.html', ):
#    import math, random
#    n = int(math.floor(100 * random.random()), )
#    y = 50
    return render_to_response(request, 'root.jinja2.html', locals(), ) #{'n':n}

## Create your views here.
#from django.shortcuts import render_to_response

#def root(request):
#    return render_to_response('root.jinja2.html')

