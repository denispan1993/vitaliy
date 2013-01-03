# coding=utf-8
__author__ = 'Sergey'

from apps.products.models import Category

def context(request):
    try:
        categories_ = Category.objects.filter(visibility=True, ).order_by('updated_at')
    except:
        categories_ = None
    try:
        categories_first_level_ = categories_.filter(parent=None, )
    except:
        categories_first_level_ = None
    return dict(request=request, categories_=categories_, categories_first_level_=categories_first_level_, )
