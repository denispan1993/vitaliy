from django.shortcuts import render_to_response
from django.template import RequestContext

def root_page(request, template_name=u'root.jinja2.html', ):
    try:
        from apps.product.models import Category
        categories_first_level_ = Category.man.first_level()
    except Category.DoesNotExist:
        categories_first_level_ = None

    return render_to_response(template_name,
        locals(),
        context_instance=RequestContext(request, ), )
