#import datetime
#import user_agents

#from django.conf import settings
#from django.forms.models import model_to_dict
from django.http import Http404, HttpResponse
#from django.http.response import HttpResponseRedirectBase
from django.views.generic.base import RedirectView, View, TemplateView
#from django_redis import get_redis_connection

#from mail.utils import decode_mid
#from stats.memory import memstat
#from stats.models import Message
#from common.utils import get_remote_addr

#from .models import Urls, Event
#from .tasks import save_event
from .models import MessageUrl, TraceOfVisits

try:
    from proj.settings import LOCAL_HOST
except ImportError:
    LOCAL_HOST = 'http://keksik.com.ua'

PIXEL_GIF = (
    'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\xff\xff\xff!\xf9\x04\x01\n'
    '\x00\x01\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02L\x01\x00;')

EMPTY_PNG = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAABmJLR0QA/wD/AP' \
            '+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3QYZCw8lAOxvjQAAABl0RVh0' \
            'Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAANSURBVAjXY2BgYGAAAAAFAAFe8yo6AAAAAElFTkSuQmCC'


class ClickView(RedirectView, ):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):

        if self.request.method == 'GET':
            key = self.request.META.get('QUERY_STRING', '')

            if key and len(key) == 64:

                try:
                    url = MessageUrl.objects.get(key=key, )

                    TraceOfVisits.objects.create(
                        now_email=url.email,
                        delivery=url.delivery,
                        type=url.url.type,
                        url=url.url.href,
                        sessionid=self.request.COOKIES.get(u'sessionid', None, ), )

                    return url.url.href

                except MessageUrl.DoesNotExist:
                    pass

        return LOCAL_HOST


class OpenView(View, ):

    def get(self, request, *args, **kwargs):
        key = kwargs['key']

        if key and len(key) == 64:

            try:
                url = MessageUrl.objects.get(key=key, )

                TraceOfVisits.objects.create(
                    now_email=url.email,
                    delivery=url.delivery,
                    type=3,
                    url=url.url.href,
                    sessionid=self.request.COOKIES.get(u'sessionid', None, ), )

            except MessageUrl.DoesNotExist:
                pass

        # return HttpResponse(PIXEL_GIF, content_type='image/gif')
        return HttpResponse(EMPTY_PNG.decode('base64'), content_type='image/png')


class UnsubView(TemplateView, ):
    template_name = 'unsub.jinja2'
