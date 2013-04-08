from django.shortcuts import render_to_response
from django.template import RequestContext


def root_page(request, template_name=u'root.jinja2.html', ):
    from apps.product.models import Category
    try:
        categories_first_level = Category.manager.first_level()
    except Category.DoesNotExist:
        categories_first_level = None

    return render_to_response(template_name=template_name,
                              dictionary=locals(),
                              context_instance=RequestContext(request, ),
                              content_type='text/html', )
