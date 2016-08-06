# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.db.models.loading import get_model
from random import randrange
from datetime import datetime, timedelta
from time import sleep

from apps.delivery.models import Delivery, MailAccount

__author__ = 'AlexStarov'


class Message(object):

    def __init__(self, delivery_pk, recipient_class, recipient_pk, **kwargs):

        self.delivery_pk = delivery_pk
        self.delivery = self.get_delivery()

        self.recipient_class = recipient_class
        self.recipient_pk = recipient_pk
        self.recipient = self.get_recipient()

        set.sender = self.get_sender()

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
        return self.delivery.subject

    def create_msg(self):
        return None

    def send(self):
        return None