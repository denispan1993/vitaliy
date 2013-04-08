# coding=utf-8
__author__ = 'Sergey'


def context(request):
    from apps.product.models import Category
    try:
        all_categories_ = Category.manager.published()
    except Category.DoesNotExist:
        all_categories_ = None

#    ajax_resolution_ = request.session.get(u'ajax_resolution', True, )

    return dict(request=request,
                all_categories_=all_categories_,
                # ajax_resolution_=ajax_resolution_,
                )
