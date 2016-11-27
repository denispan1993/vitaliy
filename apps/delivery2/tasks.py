# -*- coding: utf-8 -*-
import os
from proj.celery import celery_app
from datetime import datetime, timedelta
from celery.utils.log import get_task_logger

from django.contrib.contenttypes.models import ContentType

from time import sleep
from celery.utils import uuid
from celery.result import AsyncResult
import dns.resolver
from collections import OrderedDict

from django.db.models import Q

from apps.authModel.models import Email as AuthEmail
from apps.delivery.models import SpamEmail, MailAccount
from .models import Delivery, Message as modelMessage
from .message import Message as classMessage

#from .models import Delivery, EmailMiddleDelivery, EmailForDelivery, SpamEmail, RawEmail,\
#    Message as model_Message
#from apps.socks import models as models_socks
#from .utils import get_mail_account, get_email, create_msg, str_conv, get_email_by_str, send
#from .message import Message


__author__ = 'AlexStarov'

logger = get_task_logger(__name__)

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__), )

path = lambda base: os.path.abspath(
    os.path.join(
        PROJECT_PATH, base
    ).replace('\\', '/')
)


@celery_app.task()
def send_delivery(*args, **kwargs):
    delivery_pk = kwargs.get('delivery_pk')

    try:
        """ Исключаем:
            1. Тестовая рассылка и она отослана.
            2. Не тестовая рассылка и она отослана.
        """
        #delivery = Delivery.objects\
        #    .get(~Q(delivery_test=True, send_test=True, send_spam=False) | \
        #         ~Q(delivery_test=False, send_test=True, send_spam=True), pk=delivery_pk, )
        delivery = Delivery.objects.get(pk=delivery_pk, )
    except Delivery.DoesNotExist:
        return False

    if not delivery.can_send:
        delivery.started_at = None
        delivery.task_id = None
        delivery.save(skip_schedule=True, )
        return False

    delivery.is_active = True
    delivery.save(skip_schedule=True, )

    if delivery.delivery_test and not delivery.test_send and not delivery.general_send:

        while True:
            sleep(5)
            #auth_emails = AuthEmail.objects.filter(
            #    test=True,
            #    bad_email=False,
            #    error550=False,
            #)

            """ Берем все уже отправленные адреса (pk) из отправленных в этой рассылке """
            spam_emails_delivered = modelMessage.objects.values_list('object_id', flat=True)\
                .filter(
                delivery_id=delivery_pk,
                is_send=True,
                content_type=ContentType.objects.get_for_model(SpamEmail), )
            """ И убираем их из списка всех адресов, после чего берем один случайный pk """
            spam_emails = SpamEmail.objects.values_list('pk', flat=True)\
                .filter(
                ~Q(id__in=spam_emails_delivered),
                test=True,
                bad_email=False,
                error550=False, )\
                .order_by('?')

            if len(spam_emails) == 0:
                break

            spam_email = spam_emails[0]

            message = classMessage(
                delivery=delivery,
                recipient_class=str('{0}.{1}'.format(SpamEmail._meta.app_label, SpamEmail._meta.model_name)),
                recipient_pk=spam_email,

            )
            if message:
                print('message: True', )
                if not os.path.isfile(path('server.key', ), ):
                    mail_account = MailAccount.objects.get(pk=4)

                if message.connect(sender=mail_account, ):

                    if message.send():
                        message.save()
                    else:
                        message.delete()

            print(len(spam_emails_delivered), ' : ', len(spam_emails), ' : ', spam_email, )
#            modelMessage.objects.create(
#                delivery_id=delivery_pk,
#                email=SpamEmail.objects.get(pk=spam_email),
#                is_send=True,
#            )

#        if os.path.isfile(path('server.key', ), ):
#            real_email = get_email(delivery=delivery, email_class=Email, pk=2836, )  # pk=6, ) subscribe@keksik.com.ua
#        else:
#            real_email = get_email(delivery=delivery, email_class=Email, pk=6, )

#        #email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
#        #                                        now_email=real_email,
#        #                                        email=real_email, )
#        message = Message(test=True, delivery=delivery, recipient=real_email, )
#        print message.send()

        # mail_account = get_mail_account(pk=1, )  # subscribe@keksik.com.ua
        # msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, test=True, )
        # """ Посылаем письмо - subscribe@keksik.com.ua """
        # send(delivery=delivery, mail_account=mail_account, email=email, msg=msg)

#        """ Посылаем письмо - check-auth2@verifier.port25.com """
#        if os.path.isfile(path('server.key', ), ):
#            real_email = get_email(delivery=delivery, email_class=Email, pk=3263, )  # pk=7, ) check-auth2@verifier.port25.com
#        else:
#            real_email = get_email(delivery=delivery, email_class=Email, pk=7, )  # check-auth2@verifier.port25.com

#        message = Message(test=True, delivery=delivery, recipient=real_email, )
#        print message.send()

#        if not os.path.isfile(path('server.key', ), ):
#            real_email = get_email(delivery=delivery, email_class=SpamEmail, pk=826, )  # alex.starov@gmail.com

#        message = Message(test=True, delivery=delivery, recipient=real_email, )
#        print message.send()

#        if not os.path.isfile(path('server.key', ), ):
#            real_email = get_email(delivery=delivery, email_class=SpamEmail, pk=827, )  # starov.alex@gmail.com

#        message = Message(test=True, delivery=delivery, recipient=real_email, )
#        print message.send()

#        i = 0
#        emails = SpamEmail.objects.filter(test=True)
#        for email in emails:
#            i += 1
#            print('i: ', i, ' --> ', email.email)
#            message = Message(test=True, delivery=delivery, recipient=email, )
#            print message.send_mail()

#        emails = Email.objects.filter(test=True)
#        for email in emails:
#            i += 1
#            print('i: ', i, ' --> ', email.email)
#            message = Message(test=True, delivery=delivery, recipient=email, )
#            print message.send_mail()

#        if os.path.isfile(path('server.key', ), ):
#            recipient = get_email(delivery=delivery, email_class=SpamEmail, pk=4991, )  # gserg@mail333.com
#        else:
#            recipient = get_email(delivery=delivery, email_class=SpamEmail, pk=828, )  # gserg@mail333.com

#        message = Message(test=True, delivery=delivery, recipient=recipient, )
#        print message.send_mail()

#        if os.path.isfile(path('server.key', ), ):
#            recipient = get_email(delivery=delivery, email_class=Email, pk=2836, )  # subscribe@keksik.com.ua
#        else:
#            recipient = get_email(delivery=delivery, email_class=Email, pk=6, )  # subscribe@keksik.com.ua

#        message = Message(test=True, delivery=delivery, recipient=recipient, )
#        print message.send_mail()

#        if os.path.isfile(path('server.key', ), ):
#            recipient = get_email(delivery=delivery, email_class=Email, pk=3263, )  # check-auth2@verifier.port25.com
#        else:
#            recipient = get_email(delivery=delivery, email_class=Email, pk=7, )  # check-auth2@verifier.port25.com

#        message = Message(test=True, delivery=delivery, recipient=recipient, )
#        print message.send_mail()

#        if os.path.isfile(path('server.key', ), ):
#            recipient = get_email(delivery=delivery, email_class=Email, pk=4007, )  # check-auth@verifier.port25.com
#        else:
#            recipient = get_email(delivery=delivery, email_class=Email, pk=8, )  # check-auth@verifier.port25.com

#        message = Message(test=True, delivery=delivery, recipient=recipient, )
#        print message.send_mail()

#        if os.path.isfile(path('server.key', ), ):
#            recipient = get_email(delivery=delivery, email_class=Email, pk=4008, )  # check-auth-alex.starov=keksik.com.ua@verifier.port25.com
#        else:
#            recipient = get_email(delivery=delivery, email_class=Email, pk=9, )  # check-auth-alex.starov=keksik.com.ua@verifier.port25.com

#        message = Message(test=True, delivery=delivery, recipient=recipient, )
#        print message.send_mail()

#        if os.path.isfile(path('server.key', ), ):
#            recipient = get_email(delivery=delivery, email_class=Email, pk=4009, )  # alex.starov@gmail.com
#        else:
#            recipient = get_email(delivery=delivery, email_class=Email, pk=5, )  # alex.starov@gmail.com

#        message = Message(test=True, delivery=delivery, recipient=recipient, )
#        print message.send_mail()

#        if os.path.isfile(path('server.key', ), ):
#            recipient = get_email(delivery=delivery, email_class=SpamEmail, pk=4992, )  # webmaster@mk.mk.ua
#        else:
#            recipient = get_email(delivery=delivery, email_class=SpamEmail, pk=832, )  # webmaster@mk.mk.ua

#        message = Message(test=True, delivery=delivery, recipient=recipient, )
#        print message.send_mail()

#        if os.path.isfile(path('server.key', ), ):
#            recipient = get_email(delivery=delivery, email_class=SpamEmail, pk=4993, )  # keksik.com.ua@yandex.ru
#        else:
#            recipient = get_email(delivery=delivery, email_class=SpamEmail, pk=833, )  # keksik.com.ua@yandex.ru

#        message = Message(test=True, delivery=delivery, recipient=recipient, )
#        print message.send_mail()

#        if not os.path.isfile(path('server.key', ), ):
#            real_email = get_email(delivery=delivery, email_class=SpamEmail, pk=829, )  # krasnikov@wildpark.net

#        message = Message(test=True, delivery=delivery, recipient=real_email, )
#        print message.send()

#        if not os.path.isfile(path('server.key', ), ):
#            real_email = get_email(delivery=delivery, email_class=SpamEmail, pk=830, )  # subscribe@torta.mk.ua

#        message = Message(test=True, delivery=delivery, recipient=real_email, )
#        print message.send()

#        if not os.path.isfile(path('server.key', ), ):
#            real_email = get_email(delivery=delivery, email_class=SpamEmail, pk=831, )  # digicom-nikolaev@hotmail.com

#        message = Message(test=True, delivery=delivery, recipient=real_email, )
#        message_pk = message.get_message_pk()
#        print message.send()

#        task_set = set()

#        task = processing_delivery_through_socks.apply_async(
#            queue='delivery_send',
#            kwargs={'message_pk': message_pk, },
#            task_id='celery-task-id-{0}'.format(uuid(), ),
#        )

#        task_set.add(task.id, )

#        print(task_set)

        # email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
        #                                         now_email=real_email,
        #                                         email=real_email, )
        # send(delivery=delivery, mail_account=mail_account, email=email, msg=msg)

        """ Закрываем отсылку теста в самой рассылке """
        # delivery.send_test = True
        # delivery.save()

#    except Delivery.DoesNotExist:
#        return False

    delivery.started_at = None
    delivery.task_id = None
    delivery.is_active = True
    delivery.save(skip_schedule=True, )

    return True, datetime.now(), '__name__: {0}'.format(str(__name__))
