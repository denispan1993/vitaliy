# -*- coding: utf-8 -*-
from django_jinja.library import global_function

__author__ = 'AlexStarov'


@global_function()
def paginate_url(path_items: str, page, ) -> str:
    """

    :param path_items: QueryDict -> url path items
    :param page: int -> page number
    :return: str -> url string with page item
    """
    return_str = ''

    for i, key in enumerate(path_items):
        if i != 0 and key != 'page':
            return_str += '&'

        if key != 'page':
            return_str += '{key}={value}'.format(key=key, value=path_items[key], )

    return '?{return_str}&page={page}'.format(return_str=return_str, page=page)
