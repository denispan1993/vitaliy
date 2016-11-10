# -*- coding: utf-8 -*-
import os
import re
import socket
from copy import copy
from django.core.mail import EmailMultiAlternatives
from django.core.mail.utils import DNS_NAME
from django.core.cache import cache
from django.db.models.loading import get_model
from django.utils.html import strip_tags
from random import randrange, randint
from time import mktime
from datetime import datetime
from email.utils import formataddr
from smtplib import SMTP_SSL, SMTPException, SMTPServerDisconnected, SMTPSenderRefused, SMTPDataError

from .models import Delivery, MailAccount,\
    Message as model_Message,\
    Url,\
    MessageUrl as model_Message_Url

__author__ = 'AlexStarov'

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__), )

path = lambda base: os.path.abspath(
    os.path.join(
        PROJECT_PATH, base
    ).replace('\\', '/')
)

tokenizer_choiser = re.compile('(\[\[[\w\-\_\|\.\s]+\]\])', re.UNICODE)  # [[str1|str2]]

tokenizer_replacement = re.compile('(\{\{[\w\-\_\.\s]+\}\})')  # {{url1}}


class Message(object):

    def __init__(self, test=False,
                 delivery=None, delivery_pk=None,
                 recipient=None, recipient_class=None, recipient_pk=None,
                 **kwargs):

        self.test = test

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
        else:
            self.recipient_class = recipient_class
            self.recipient_pk = recipient_pk
            self.recipient = self.get_recipient()

        self.recipient_content_type = self.recipient.content_type
        self.recipient_type = self.get_recipient_type()

        if os.path.isfile(path('server.key', ), ):
            self.sender = MailAccount.objects.get(pk=34, )
        else:
            self.sender = MailAccount.objects.get(pk=4, )

        self.subject_pk, self.subject = self.get_subject()

        self.message_pk, self.message = self.create_message()

        self.qs_message_urls, self.dict_urls = self.create_message_urls()

        self.inst_unsub_url, self.dict_urls['unsub'] = self.create_unsub_url()
        self.inst_open_tag, self.dict_urls['open'] = self.create_open_tag()

        self.body_raw = self.get_body_raw()
        self.body_finished = self.get_body_finished()

        """ did - Delivery id """
        self.did = self.get_did()
        """ eid - Email id """
        self.eid = self.get_eid()
        """ mid - Message id """
        self.mid = self.get_mid()

        """ Reply-To + Return-Path """
        """ X-Campaign-Id - EmailStream.ru """
        """ List-id - postoffice.yandex.ru """
        self.headers = {
            'Return-Path': 'postmaster@keksik.com.ua',
            'Reply-To': 'postmaster@keksik.com.ua',
            'X-Campaign-Id': self.did,
            'X-Delivery-id': self.did,
            'X-Email-id': self.eid,
            'X-Message-id': self.mid,
            'List-Unsubscribe': self.dict_urls['unsub'],
        }

        self.message = self.create_msg()
        self.connection = self.connect()

    def get_message_pk(self, ):
        return self.message_pk

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

    def get_recipient_type(self):
        """ eid - Email id
            1 - Нормальные E-Mail
            2 - Spam E-Mail """
        if self.recipient_class.split('.')[1] == 'Email':
            return 1
        elif self.recipient_class.split('.')[1] == 'SpamEmail':
            return 2
        else:
            return 0

    def get_recipient_pk(self):
        return self.recipient.pk

    def get_sender_email(self):
        return 'sender-email-{0}@keksik.com.ua'.format(self.mid, )

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

        return subject.pk, self.choice_str_in_tmpl(tmpl=subject.subject)

    def create_message(self):
        message = model_Message.objects.create(
            delivery_id=self.delivery_pk,
            email=self.recipient,
        )
        return message.pk, message

    def create_message_urls(self):
        for url in Url.objects.filter(
                delivery=self.delivery,
                type=1, ):
            model_Message_Url.objects.create(
                delivery_id=self.delivery_pk,
                url_id=url.pk,
                message_id=self.message_pk,
                email=self.recipient,
                # content_type=self.recipient_content_type,
                # object_id=self.recipient_pk
            )

        qs_urls = model_Message_Url.objects.filter(
            url__type=1,
            delivery_id=self.delivery_pk,
            message_id=self.message_pk,
            content_type=self.recipient_content_type,
            object_id=self.recipient_pk
        )
        dict_urls = {}
        for url in qs_urls:
            dict_urls['url{}'.format(url.url.url_id, )] = url.ready_url_str

        return qs_urls, dict_urls

    def create_unsub_url(self):
        url = cache.get('unsub_url_{}'.format(self.delivery_pk), False)

        if not url:
            url, create = Url.objects.get_or_create(
                delivery_id=self.delivery_pk,
                href='http://keksik.com.ua/delivery/unsubscribe/',
                type=2,
            )

            cache.set(
                key='unsub_url_{}'.format(self.delivery_pk),
                value=url,
                timeout=259200, )  # 60 sec * 60 min * 24 hour * 3

        inst_unsub = model_Message_Url.objects.create(
            delivery_id=self.delivery_pk,
            url_id=url.pk,
            message_id=self.message_pk,
            email=self.recipient,
        )

        return inst_unsub, inst_unsub.ready_url_str

    def create_open_tag(self):
        url = cache.get('open_url_{0}'.format(self.delivery_pk), False)

        if not url:
            url, create = Url.objects.get_or_create(
                delivery_id=self.delivery_pk,
                href='http://keksik.com.ua/delivery/open/',
                type=3,
            )

            cache.set(
                key='open_url_{0}'.format(self.delivery_pk),
                value=url,
                timeout=259200, )  # 60 sec * 60 min * 24 hour * 3

        inst_open = model_Message_Url.objects.create(
            delivery_id=self.delivery_pk,
            url_id=url.pk,
            message_id=self.message_pk,
            email=self.recipient,
        )

        return inst_open, inst_open.ready_url_str

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

        body_finished = self.replace_str_in_tmpl(
            tmpl=body_finished,
            context=self.dict_urls, )

        return body_finished

    def choice_str_in_tmpl(self, tmpl, ):
        """ ccc('aaa [[bbb|111]] ccc [[ddd|222]] eee [[fff|333|444|555|666]] ggg') """

        three = re.split(tokenizer_choiser, tmpl)

        nodes = {}
        for pos, block in enumerate(three):
            if block.startswith('[[') and block.endswith(']]'):
                keys = block.strip('[[]]').split('|')
                """ Выборка СЛУЧАЙНОГО значения """
                value = keys[randrange(start=0, stop=len(keys))]

                if pos not in nodes:
                    nodes[pos] = value

        three = copy(three)

        for pos, value in nodes.iteritems():

            three[pos] = value

        return ''.join(three)

    def replace_str_in_tmpl(
            self,
            tmpl,
            context={
                'url1': '<a href="http://keksik.com.ua/>www.keksik.com.ua</a>',
            },
    ):
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

        return ''.join(three)

    def get_did(self, ):
        """ did - Delivery id """
        return '{0:04d}-{1:02d}'.format(self.delivery_pk, self.delivery.type, )

    def get_eid(self, ):
        """ eid - Email id """
        return '{0:02d}-{1:07d}'.format(self.recipient_type, self.recipient_pk, )

    def get_mid(self, ):
        """ mid - Message id """  # -{3:06x} - randint(0, 999999),
        return '{0}-{1}-{2:010d}'\
            .format(self.did, self.eid, int(mktime(datetime.now().timetuple())), )

    def create_msg(self, ):
        message_kwargs = {
            'from_email': formataddr(
                (u'Интернет магаизн Keksik', self.get_sender_email()), ),
            'to': [self.recipient.email, ],
            'headers': self.headers,
            'subject': u'test - {}'.format(self.subject) if self.test else self.subject,
            'body': strip_tags(self.body_finished, ),
        }

        message = EmailMultiAlternatives(**message_kwargs)
        message.attach_alternative(content=self.body_finished, mimetype='text/html', )

        return message.message()

    def connect(self, ):
        connection_class = SMTP_SSL
        connection_params = {'local_hostname': DNS_NAME.get_fqdn()}

        try:
            connection = connection_class(
                host=self.sender.server.server_smtp,
                port=self.sender.server.port_smtp,
                **connection_params)

            if self.sender.username and self.sender.password:
                connection.login(self.sender.username, self.sender.password, )
                connection.ehlo()

            return connection

        except (SMTPException, SMTPServerDisconnected) as e:
            print('Exception(SMTPException, SMTPServerDisconnected): ', e)
            return False

        except socket.error as e:
            print('Exception(socket.error): ', e)
            return False

    def send_mail(self, ):
        try:
            self.connection.sendmail(
                from_addr=formataddr(
                    (u'Интернет магаизн Keksik', self.get_sender_email())),
                to_addrs=[self.recipient.email, ],
                msg=self.message.as_string(), )
            self.connection.quit()

            return True

        except SMTPSenderRefused as e:
            print('SMTPSenderRefused: ', e)

        except SMTPDataError as e:
            print('SMTPDataError: ', e, ' messages: ', e.message, ' smtp_code: ', e.smtp_code, 'smtp_error: ', e.smtp_error, ' args: ', e.args)

            if e.smtp_code == 554 and\
                    "5.7.1 Message rejected under suspicion of SPAM; https://ya.cc/" in e.smtp_error:
                print('SPAM Bloked E-Mail: ', self.recipient, ' NOW !!!!!!!!!!!!!!!!!!!!!!!')
                self.recipient.is_auto_active = False
                self.recipient.auto_active_datetime = datetime.now()
                self.recipient.save()

        except Exception as e:
            print('Exception: ', e)

        return False
