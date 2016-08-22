import datetime
#import user_agents

from django.conf import settings
from django.forms.models import model_to_dict
from django.http import Http404, HttpResponse
from django.http.response import HttpResponseRedirectBase
from django.views.generic.base import RedirectView, View
#from django_redis import get_redis_connection

#from mail.utils import decode_mid
#from stats.memory import memstat
#from stats.models import Message
#from common.utils import get_remote_addr

#from .models import Urls, Event
#from .tasks import save_event
from .models import MessageUrl, TraceOfVisits

PIXEL_GIF = (
    'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\xff\xff\xff!\xf9\x04\x01\n'
    '\x00\x01\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02L\x01\x00;')


class ClickView(RedirectView, ):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):

        if self.request.method == 'GET':
            query_string = self.request.META.get('QUERY_STRING', '')

            if query_string and len(query_string) == 64:

                try:
                    url = MessageUrl.objects.get(key=query_string, )

                    TraceOfVisits.objects.create(
                        email=url.email,
                        delivery=url.delivery,
                        url=url.url.href,
                        sessionid=self.request.COOKIES.get(u'sessionid', None, ), )

                    return url.url.href

                except MessageUrl.DoesNotExist:
                    pass

        return 'http://keksik.com.ua'


class OpenView(View, ):

    def get(self, request, *args, **kwargs):
        message = self.get_message(kwargs['mid'])

        if not self.is_event_exists(kwargs['mid']):
            self.save_event(message, **kwargs)

        return HttpResponse(PIXEL_GIF, content_type='image/gif')
