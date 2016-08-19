# -*- coding: utf-8 -*-
import re
from copy import copy
from django.core.mail import get_connection, EmailMultiAlternatives
from django.core.mail.utils import DNS_NAME
from django.core.cache import cache
from django.db.models.loading import get_model
from django.utils.html import strip_tags
from random import randrange, randint
from time import mktime
from datetime import datetime, timedelta
from time import sleep
import dns.resolver
from email.utils import formataddr
from smtplib import SMTP, SMTP_SSL, SMTPException, SMTPServerDisconnected, SMTPSenderRefused, SMTPDataError

from .models import Delivery, MailAccount,\
    Message as model_Message,\
    Url,\
    MessageUrl as model_Message_Url

__author__ = 'AlexStarov'


tokenizer_choiser = re.compile('(\[[\[a-z|A-Z0-9\-\_\.]+\]])', re.MULTILINE)  # [[str1|str2]]
tokenizer_replacement = re.compile('(\{{[a-zA-Z0-9\-\_\.]+\}})', re.MULTILINE)  # {{url1}}


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

        self.subject_pk, self.subject = self.get_subject()

        self.message_pk, self.message = self.create_message()

        self.qs_message_urls, self.dict_message_urls = self.create_message_urls()

        self.body_raw = self.get_body_raw()
        self.body_finished = self.get_body_finished()

        """ did - Delivery id """
        self.did = self.get_did()
        """ eid - Email id """
        self.eid = self.get_eid()
        """ mid - Message id """
        self.mid = self.get_mid()
        """ Reply-To + Return-Path """
        self.headers = {
            'X-Delivery-id': self.did,
            'X-Email-id': self.eid,
            'X-Message-id': self.mid,
        }

        if self.recipient.domain in ['keksik.com.ua', 'yandex.ru', 'yandex.ua', ]:
            self.sender = self.get_sender()
            self.message = self.create_msg(directly=False, )
            self.headers['Return-Path'] = self.sender.get_return_path_subscribe,
            self.headers['Reply-To'] = self.sender.get_return_path_subscribe,
            self.send_mail_through()
#        else:
#            self.MXes = self.get_MXes()
#            self.message = self.create_msg(directly=True, )
#            if not self.send_mail_direct():
#                self.message = self.create_msg(directly=False, )
#                self.send_mail_through()


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

                sender = senders.get(pk=sender_id, )

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
        return message.pk, message

    def create_message_urls(self):
        qs_urls = model_Message_Url.objects.bulk_create([
            model_Message_Url(
                delivery_id=self.delivery_pk,
                url=url,
                message_id=self.message_pk,
                content_type=self.recipient_content_type,
                object_id=self.recipient_pk
            )
            for url in Url.objects.filter(delivery=self.delivery, )]
        )
        dict_urls = {}
        for url in qs_urls:
            dict_urls['url{}'.format(url.url_id, )] = url.ready_url_str

        return qs_urls, dict_urls

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

        print('get_body_raw(body.html): ', body.raw, )
        return body.html

    def get_body_finished(self):
        body_finished = self.choice_str_in_tmpl(self.body_raw)

        print('get_body_finished(body_finished): (1)', body_finished, )

        body_finished = self.replace_str_in_tmpl(
            tmpl=body_finished,
            context=self.dict_message_urls, )

        print('get_body_finished(body_finished): (2)', body_finished, )

        return body_finished

    def choice_str_in_tmpl(self, tmpl, ):
        """ ccc('aaa [[bbb|111]] ccc [[ddd|222]] eee [[fff|333|444|555|666]] ggg') """

        three = re.split(tokenizer_choiser, tmpl)

        print('choice_str_in_tmpl(three): (1)', three)

        nodes = {}
        for pos, block in enumerate(three):
            if block.startswith('[[') and block.endswith(']]'):
                keys = block.strip('[[]]').split('|')

                value = keys[randrange(start=0, stop=len(keys))]

                if pos not in nodes:
                    nodes[pos] = value

        print('choice_str_in_tmpl(nodes): ', nodes)

        three = copy(three)

        for pos, value in nodes.iteritems():

            three[pos] = value

        print('choice_str_in_tmpl(three): (2)', three)

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
        return '{0:04d}-{0:02d}'.format(self.delivery_pk, self.delivery.type, )

    def get_eid(self, ):
        """ eid - Email id """
        return '{0:02d}-{1:07d}'.format(self.recipient_type, self.recipient_pk, )

    def get_mid(self, ):
        """ mid - Message id """
        return '{0}-{1}-{2:011x}-{3:x}'\
            .format(self.did, self.eid, int(mktime(datetime.now().timetuple())), randint(0, 10000000), )

    def get_MXes(self, ):
        answers = dns.resolver.query(self.recipient.domain, 'MX')
        return sorted({rdata.preference: rdata.exchange for rdata in answers})

    def get_email_send_direct(self, ):
        return u'{}@keksik.com.ua'.format(self.mid, )

    def create_msg(self, directly=True, ):
        message_kwargs = {
            'from_email': formataddr(
                (u'Интернет магаизн Keksik',
                 self.get_email_send_direct() if directly else self.get_sender().email)),
            'to': [self.recipient.email, ],
            'headers': self.headers,
            'subject': u'test - {}'.format(self.subject) if self.test else self.subject,
            'body': strip_tags(self.body_finished, ),
        }

        message = EmailMultiAlternatives(**message_kwargs)
        message.attach_alternative(content=self.body_finished , mimetype='text/html')

        return message.message()

    def send_mail_through(self):
        try:
            connection_class = SMTP_SSL if self.sender.server.use_ssl_smtp and \
                                           not self.sender.server.use_tls_smtp else SMTP
            connection_params = {'local_hostname': DNS_NAME.get_fqdn()}

            # if timeout:
            #     connection_params['timeout'] = timeout

            try:
                connection = connection_class(host=self.sender.server.server_smtp,
                                              port=self.sender.server.port_smtp,
                                              **connection_params)
                if not self.sender.server.use_ssl_smtp and self.sender.server.use_tls_smtp:
                    connection.ehlo()
                    connection.starttls()
                    connection.ehlo()
                if self.sender.username and self.sender.password:
                    connection.login(self.sender.username, self.sender.password, )

                connection.sendmail(from_addr=self.sender.email,
                                    to_addrs=[self.recipient.email, ],
                                    msg=self.message.as_string(), )
                connection.quit()

            except (SMTPException, SMTPServerDisconnected):
                pass
                # if not fail_silently:
                #     raise
                # else:
                #     return False

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

                # connection = connect(mail_account=mail_account, fail_silently=True, )
                # msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, exception=e, test=True, )
                # send_msg(connection=connection, mail_account=mail_account, email=email, msg=msg, )

        except Exception as e:
            print('Exception: ', e)

        return False
