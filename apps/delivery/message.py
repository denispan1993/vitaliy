# -*- coding: utf-8 -*-
import re
from copy import copy
from django.core.cache import cache
from django.db.models.loading import get_model
from random import randrange
from datetime import datetime, timedelta
from time import sleep

from .models import Delivery, MailAccount,\
    Message as model_Message,\
    Url,\
    MessageUrl as model_Message_Url

__author__ = 'AlexStarov'


tokenizer_choiser = re.compile('(\[[\[a-z|A-Z0-9\-\_\.]+\]])', re.MULTILINE)  # [[str1|str2]]
tokenizer_replacement = re.compile('(\{{[a-zA-Z0-9\-\_\.]+\}})', re.MULTILINE)  # {{url1}}


class Message(object):

    def __init__(self, delivery=None, delivery_pk=None,
                 recipient=None, recipient_class=None, recipient_pk=None,
                 **kwargs):

        if delivery:
            self.delivery = delivery
            self.delivery_pk = delivery.pk
        else:
            self.delivery_pk = delivery_pk
            self.delivery = self.get_delivery()

        if recipient:
            self.recipient = recipient
            self.recipient_class = self.get_recipient_class()
            self.recipient_pk = self.get_recipient_pk()
            self.recipient_content_type = self.recipient.content_type
        else:
            self.recipient_class = recipient_class
            self.recipient_pk = recipient_pk
            self.recipient = self.get_recipient()
            self.recipient_content_type = self.recipient.content_type

        self.subject_pk, self.subject = self.get_subject()

        self.message = self.create_message()

        self.message_urls = self.create_message_urls()

        self.body_raw = self.get_body_raw()
        self.body_complit = self.get_body_complit()

        self.sender = self.get_sender()

        #self.msg = create_msg(delivery=delivery, mail_account=mail_account, email=email_for, test=False, )

    def get_delivery(self):

        delivery = cache.get(
            key='delivery_pk_{0}'.format(self.delivery_pk, ), )

        if delivery:
            return delivery

        else:
            delivery = Delivery.objects.get(pk=self.delivery_pk)
            cache.set(
                key='delivery_pk_{0}'.format(self.delivery_pk, ),
                value=delivery,
                timeout=259200, )  # 60 sec * 60 min * 24 hour * 3

            return delivery

    def get_recipient(self):
        email_model = get_model(*self.recipient_class.split('.'))

        return email_model.objects.get(pk=self.recipient_pk, )

    def get_recipient_class(self):
        return str('{0}.{1}'.format(self.recipient._meta.app_label, self.recipient.__class__.__name__))

    def get_recipient_pk(self):
        return self.recipient.pk

    def get_sender(self):
        senders = cache.get(key='senders', )

        if not senders:
            senders = MailAccount.objects.filter(server__use_smtp=True, use_smtp=True, ).order_by('?')

            cache.set(
                key='senders',
                value=senders,
                timeout=259200, )  # 60 sec * 60 min * 24 hour * 3

        len_senders = senders.values_list('pk', flat=True).latest('id', )
        i = 0
        while True:
            sender_id = randrange(1, len_senders, )
            i += 1
            try:

                sender = senders[sender_id, ]

                if sender.is_auto_active:
                    return sender
                else:
                    print('==============| ', 'Sender: ', sender, ' |================')
                    print('TimeDelta: timedelta(hours=2, ): ', timedelta(hours=2, ))
                    print('sender.auto_active_datetime: ', sender.auto_active_datetime)
                    print('sender.auto_active_datetime.replace(tzinfo=None): ', sender.auto_active_datetime.replace(tzinfo=None, ))
                    bbb = sender.auto_active_datetime.replace(tzinfo=None, ) + timedelta(hours=2, )
                    print('sender.auto_active_datetime.replace(tzinfo=None) + TimeDelta(hours=2, ): ', bbb)
                    print('datetime.now(): ', datetime.now())
                    print('datetime.now().replace(tzinfo=None, ): ', datetime.now().replace(tzinfo=None, ))
                    print('===================================================================')
                    """ Берем дататайм из базы,
                        убираем часовой пояс,
                        + 2 часа нашего часового пояса,
                        + смещение 1 день 1 час 30 минут """
                    datetime_delta = sender.auto_active_datetime.\
                                         replace(tzinfo=None, )\
                                         + timedelta(hours=2, )\
                                         + timedelta(days=1, hours=1, minutes=30, )
                    if datetime_delta < datetime.now():
                        sender.is_auto_active = True
                        sender.save()
                        cache.delete('senders')
                        print('MailAccount: ', sender)
                        return sender

            except IndexError:
                pass

            sleep(1)
            if i > 50:
                """ Если нету свободных почтовых аккаунтов,
                    то ждем пол часа и выходим """
                sleep(86400, )  # 3600 * 24h
                return False

    def get_subject(self):
        subject_value, subject_value_pk = 5000000, 0

        subjects = self.delivery.subject_set.all().order_by('pk', )

        for subject in subjects:
            try:
                subject_cache_value = cache.get_or_set(
                    key='subject_cache_pk_{0}'.format(subject.pk, ),
                    value=subject.chance,
                    timeout=259200, )

            except AttributeError:
                subject_cache_value = cache.get(
                    key='subject_cache_pk_{0}'.format(subject.pk, ), )

                if not subject_cache_value:
                    subject_cache_value = subject.chance
                    cache.set(
                        key='subject_cache_pk_{0}'.format(subject.pk, ),
                        value=subject.chance,
                        timeout=259200, )  # 60 sec * 60 min * 24 hour * 3

            if subject_cache_value < subject_value:
                subject_value, subject_value_pk = subject_cache_value, subject.pk

        subject = subjects.get(pk=subject_value_pk, )
        cache.set(
            key='subject_cache_pk_{0}'.format(subject.pk, ),
            value=subject_cache_value + subject.chance,
            timeout=259200, )  # 60 sec * 60 min * 24 hour * 3

        return subject.pk, subject.subject

    def create_message(self):
        message = model_Message.objects.create(
            delivery_id=self.delivery_pk)
        return message

    def create_message_urls(self):
        try:
            urls = Url.objects.filter(delivery=self.delivery, )
        except Url.DoesNotExist:
            return {}

        dict_urls = {}
        for url in urls:
            dict_urls['url{}'.format(url.url_id, )] = model_Message_Url.objects.create(
                delivery_id=self.delivery_pk,
                url=url,
                content_type=self.recipient_content_type,
                object_id=self.recipient_pk
            )

        return dict_urls

    def get_body_raw(self):
        body_value, body_value_pk = 5000000, 0

        bodies = self.delivery.body_set.all().order_by('pk', )

        for body in bodies:
            try:
                body_cache_value = cache.get_or_set(
                    key='body_cache_pk_{0}'.format(body.pk, ),
                    value=body.chance,
                    timeout=259200, )

            except AttributeError:
                body_cache_value = cache.get(
                    key='body_cache_pk_{0}'.format(body.pk, ), )

                if not body_cache_value:
                    body_cache_value = body.chance
                    cache.set(
                        key='body_cache_pk_{0}'.format(body.pk, ),
                        value=body.chance,
                        timeout=259200, )  # 60 sec * 60 min * 24 hour * 3

            if body_cache_value < body_value:
                body_value, body_value_pk = body_cache_value, body.pk

        body = bodies.get(pk=body_value_pk, )
        cache.set(
            key='body_cache_pk_{0}'.format(body.pk, ),
            value=body_cache_value + body.chance,
            timeout=259200, )  # 60 sec * 60 min * 24 hour * 3

        return body.html

    def get_body_finished(self):
        body_finished = self.choice_str_in_tmpl(self.body_raw)
        try:
            urls = Url.objects.filter(delivery=self.delivery, )
        except Url.DoesNotExist:
            return []

        urls_dict = {}
        for url in urls:
            urls_dict['url'] = render_to_string(template_name='render_img_string.jinja2', context=url, )

        return body_finished

    def choice_str_in_tmpl(self, tmpl, ):
        """ ccc('aaa [[bbb|111]] ccc [[ddd|222]] eee [[fff|333|444|555|666]] ggg') """

        three = re.split(tokenizer_choiser, tmpl)

        nodes = {}
        for pos, block in enumerate(three):
            if block.startswith('[[') and block.endswith(']]'):
                keys = block.strip('[[]]').split('|')

                value = keys[randrange(start=0, stop=len(keys))]

                if pos not in nodes:
                    nodes[pos] = value

        three = copy(three)
        for pos, value in nodes.iteritems():

            three[pos] = value

        return ''.join(three)

    def replace_str_in_tmpl(self, tmpl, context={}, ):
        """ bbb('aaa {{aaa1}} ccc {{bbb2}} eee {{ccc3}} ggg', {'aaa1': '1aaa', 'bbb2': 'bb2b', 'ccc3': 'ccc333ccc', }) """

        three = re.split(tokenizer_replacement, tmpl)

        nodes = {}
        for pos, block in enumerate(three):
            if block.startswith('{{') and block.endswith('}}'):
                key = block.strip('{{}}')

                if key not in nodes:
                    nodes[key] = []
                nodes[key].append(pos)

        keys = nodes.keys()
        three = copy(three)
        for key, value in context.iteritems():
            if key in keys:
                for pos in nodes[key]:
                    three[pos] = value

        print ''.join(three)

    def create_msg(self):
        return None

    def send(self):
        return None