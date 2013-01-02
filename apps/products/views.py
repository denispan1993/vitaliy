# Create your views here.
from django.shortcuts import render_to_response

def show_category(request,
                  category_url,
                  id,
                  template_name=u'category/show_category.jinja2.html',
                  ):
    return render_to_response('category/show_category.jinja2.html')


def show_product(request,
                 product_url,
                 id,
                 template_name=u'product/show_product.jinja2.html',
                ):
    return render_to_response('pruduct/show_product.html')