# coding=utf-8
__author__ = 'Sergey'


def context(request):
#    from apps.product.models import Category
#    try:
#        all_categories_ = Category.manager.published()
#    except Category.DoesNotExist:
#        all_categories_ = None

#    ajax_resolution_ = request.session.get(u'ajax_resolution', True, )

    from apps.product.models import Category
    try:
        categories_basement_ = Category.manager.basement()
    except Category.DoesNotExist:
        categories_basement_ = None

    return dict(request=request,
                categories_basement_=categories_basement_,
                # ajax_resolution_=ajax_resolution_,
                )
