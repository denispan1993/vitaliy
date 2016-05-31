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

PIXEL_GIF = (
    'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\xff\xff\xff!\xf9\x04\x01\n'
    '\x00\x01\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02L\x01\x00;')


class ClickView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        t = int(kwargs['hash'][24:], 16)
        date = datetime.datetime.fromtimestamp(t)

        message = self.get_message(kwargs['mid'])
        redirect_url = self.redis.get('urls:{}'.format(kwargs['hash'][:24]))

        if not redirect_url:
            try:
                urls = Urls.objects.get(hash=kwargs['hash'], created=date)
            except Urls.DoesNotExist:
                raise Http404
            else:
                redirect_url = urls.redirect_url

        if not self.is_event_exists(kwargs['mid'], kwargs['hash']):
            self.save_event(message, **kwargs)

        return redirect_url


class OpenView(View):

    def get(self, request, *args, **kwargs):
        message = self.get_message(kwargs['mid'])

        if not self.is_event_exists(kwargs['mid']):
            self.save_event(message, **kwargs)

        return HttpResponse(PIXEL_GIF, content_type='image/gif')
