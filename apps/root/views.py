from django.shortcuts import render_to_response
from django.template import RequestContext

def root_page(request, template_name='root.jinja2.html', ):
    return render_to_response('root.jinja2.html',
        locals(),
        context_instance=RequestContext(request, ), )
