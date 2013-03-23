# coding=utf-8
__author__ = 'Sergey'


def context(request):
    try:
        from apps.product.models import Category
        categories_ = Category.man.published()
    except Category.DoesNotExist:
        categories_ = None

#    ajax_resolution_ = request.session.get(u'ajax_resolution', True, )

    return dict(request=request,
                categories_=categories_,
                # ajax_resolution_=ajax_resolution_,
                )
