# coding=utf-8
__author__ = 'Sergey'


def context(request):
    try:
        from apps.product.models import Category
        categories_ = Category.man.published()
    except Category.DoesNotExist:
        categories_ = None

    return dict(request=request, categories_=categories_, )
