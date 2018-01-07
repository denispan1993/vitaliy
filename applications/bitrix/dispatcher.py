# -*- coding: utf-8 -*-

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

from .auth_decorators import has_perm_or_basicauth, logged_in_or_basicauth
from .auth_process import check_auth
from .http_process import init, upload_file, import_file, export_query, export_success

__author__ = 'AlexStarov'


@csrf_exempt
@has_perm_or_basicauth('cml.add_exchange')
@logged_in_or_basicauth()
def front_view(request):
    return Dispatcher().dispatch(request)


class Dispatcher(object):
    def __init__(self):
        self.routes_map = {
            (u'catalog', u'checkauth'): check_auth,
            (u'catalog', u'init'): init,
            (u'catalog', u'file'): upload_file,
            (u'catalog', u'import'): import_file,
            (u'sale', u'file'): upload_file,
            (u'import', u'import'): import_file,
            (u'sale', u'checkauth'): check_auth,
            (u'sale', u'init'): init,
            (u'sale', u'query'): export_query,
            (u'sale', u'success'): export_success,
        }

    def dispatch(self, request):
        view_key = (request.GET.get('type'), request.GET.get('mode'))
        view = self.routes_map.get(view_key)
        if not view:
            raise Http404
        return view(request)
