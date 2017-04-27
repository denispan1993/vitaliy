# -*- coding: utf-8 -*-
from django_jinja.library import global_function
from django.core.cache import cache

__author__ = 'AlexStarov'


@global_function()
def queryset_filter(parent, qs, ):

    key = 'category_children_{0}'.format(parent.id)
    return_queryset = cache.get(key=key, )

    if not return_queryset:

        return_queryset = qs.filter(parent_id=parent.id, )
        cache.set(key=key,
                  value=return_queryset,
                  timeout=3600, )

    return return_queryset
