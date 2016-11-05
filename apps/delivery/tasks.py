# -*- coding: utf-8 -*-
import os
from proj.celery import celery_app
from datetime import datetime, timedelta
from celery.utils.log import get_task_logger
from time import sleep
from celery.utils import uuid
from celery.result import AsyncResult
import dns.resolver
from collections import OrderedDict

from django.db.models import Q

import email
from imaplib import IMAP4_SSL

from apps.authModel.models import Email
from .models import Delivery, EmailMiddleDelivery, EmailForDelivery, SpamEmail, RawEmail,\
    Message as model_Message
from apps.socks import models as models_socks
from .utils import get_mail_account, get_email, create_msg, str_conv, get_email_by_str, send
from .message import Message

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__), )

path = lambda base: os.path.abspath(
    os.path.join(
        PROJECT_PATH, base
    ).replace('\\', '/')
)

reason550 = {'google.com': 'said: 550-5.1.1 The email account that you tried to reach does not exist.',
             'GOOGLE.COM': 'said: 550 5.2.1 The email account that you tried to reach is disabled.',
             'mail.ru': 'said: 550 Message was not accepted -- invalid mailbox. Local mailbox',
             'mail.ru': 'said: 550 5.1.1 Bad destination mailbox address: invalid mailbox. Local mailbox',
             'ukr.net': 'said: 550-Message for',
             'i.ua': 'said: 550 Mailbox is frozen.',
             'bigmir.net': 'said: 550 Mailbox is frozen.',
             'qip.ru': 'said: 550 Addresses failed:',
             'rambler.ru': ': Recipient address rejected: Account deleted by user (in reply to RCPT TO command)',

             'tuhs.org': 'Recipient address rejected: User unknown in local recipient table (in reply to RCPT TO command)',
             '127.0.0.1': 'said: 554 5.1.1 Unknown user;',
             'mts.com.ua': 'said: 550 #5.1.0 Address rejected. (in reply to RCPT TO command)',
             'cummins-power.com.ua': 'said: 550 5.2.1 Mailbox unavailable. This server does not accept mails from this sender address (',
             'dalgakiran.com.ua': 'said: 550 5.2.1 Mailbox unavailable. This server does not accept mails from this sender address (',
             'cook-time.com': 'said: 550 No Such User Here',
             'wr0.ru': 'said: 554 5.7.1',
             }


@celery_app.task()
def processing_delivery_test(*args, **kwargs):
    delivery_pk = kwargs.get('delivery_pk')

    try:
        """ Исключаем:
            1. Тестовая рассылка и она отослана.
            2. Не тестовая рассылка и она отослана.
        """
        delivery = Delivery.objects\
            .get(~Q(delivery_test=True, send_test=True, send_spam=False) | \
                 ~Q(delivery_test=False, send_test=True, send_spam=True), pk=delivery_pk, )

        """ Создаем ссылочку на отсылку рассылки """
        # email_middle_delivery = EmailMiddleDelivery.objects.create(delivery=delivery,
        #                                                            delivery_test_send=True,
        #                                                            delivery_send=False, )

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

        i = 0
        emails = SpamEmail.objects.filter(test=True)
        for email in emails:
            i += 1
            print('i: ', i, ' --> ', email.email)
            message = Message(test=True, delivery=delivery, recipient=email, )
            print message.send_mail()

        emails = Email.objects.filter(test=True)
        for email in emails:
            i += 1
            print('i: ', i, ' --> ', email.email)
            message = Message(test=True, delivery=delivery, recipient=email, )
            print message.send_mail()

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

    except Delivery.DoesNotExist:
        return False

    return True, datetime.now(), '__name__: {0}'.format(str(__name__))


@celery_app.task()
def processing_delivery_real(*args, **kwargs):
    start = datetime.now()
    delivery_pk = kwargs.get('delivery_pk')

    try:
        """ Исключаем:
            1. Тестовая рассылка и она отослана.
            2. Не тестовая рассылка и она отослана.
        """
        delivery = Delivery.objects\
            .get(~Q(delivery_test=True, send_test=True, send_spam=False) | \
                 ~Q(delivery_test=False, send_test=True, send_spam=True), pk=delivery_pk, )

        """ Создаем ссылочку на отсылку рассылки """
        email_middle_delivery = EmailMiddleDelivery.objects.create(delivery=delivery,
                                                                   delivery_test_send=False,
                                                                   spam_send=True,
                                                                   delivery_send=False, )

        try:
            query_emails = Email.objects\
                .filter(bad_email=False, error550=False, )\
                .order_by('?')
            query_spam_emails = SpamEmail.objects\
                .filter(bad_email=False, error550=False, )\
                .order_by('?')

        except Email.DoesNotExist:
            return False, datetime.now()

        query_emails_list = set(obj.pk for obj in query_emails)
        query_spam_emails_list = set(obj.pk for obj in query_spam_emails)

        task_set = set()
        while True:
            if len(query_emails_list) > 0 and len(task_set) < 20:
                real_email, query_emails_list, query_emails = get_email(
                    delivery=delivery,
                    email_class=str('{0}.{1}'.format(Email._meta.app_label, Email.__name__)),
                    queryset_list=query_emails_list,
                    queryset=query_emails,
                )

                if real_email:
                    task = processing_delivery.apply_async(
                        queue='delivery_send',
                        kwargs={'delivery_pk': delivery.pk,
                                'email_middle_delivery_pk': email_middle_delivery.pk,
                                'email_class': str('{0}.{1}'.format(Email._meta.app_label, Email.__name__)),
                                'email_pk': real_email.pk, },
                        task_id='celery-task-id-{0}'.format(uuid(), ),
                    )

                    logger.info(u'Task.id : {0} --> app_label: {1} model: {2} --> email: {3}'
                                .format(task.id, Email._meta.app_label, Email.__name__, real_email.email, ), )

                    task_set.add(task.id, )

            if len(query_spam_emails_list) > 0 and len(task_set) < 20:
                real_email, query_spam_emails_list, query_spam_emails = get_email(
                    delivery=delivery,
                    email_class=str('{0}.{1}'.format(SpamEmail._meta.app_label, SpamEmail.__name__)),
                    queryset_list=query_spam_emails_list,
                    queryset=query_spam_emails,
                )

                if real_email:
                    task = processing_delivery.apply_async(
                        queue='delivery_send',
                        kwargs={'delivery_pk': delivery.pk,
                                'email_middle_delivery_pk': email_middle_delivery.pk,
                                'email_class': str('{0}.{1}'.format(SpamEmail._meta.app_label, SpamEmail.__name__)),
                                'email_pk': real_email.pk, },
                        task_id='celery-task-id-{0}'.format(uuid(), ),
                    )

                    logger.info(u'Task.id : {0} --> app_label: {1} model: {2} --> email: {3}'
                                .format(task.id, SpamEmail._meta.app_label, SpamEmail.__name__, real_email.email, ), )

                    task_set.add(task.id, )

            """ Бежим по task.id и проверяем степень готовности """
            for task_id in task_set.copy():
                sleep(4)

                task = AsyncResult(task_id, )
                if task.status == 'SUCCESS':

                    task_set.remove(task_id)

                    task_result_dict = task.result
                    print('REMOVE!!!!!!!!! --> ', 'task_id: ', task_id, 'task.status: ', task.status, 'task_result_dict: ', task_result_dict)

                    if isinstance(task_result_dict['result'], bool) and task_result_dict['result'] is False:
                        print("task_result_dict['result']: ", task_result_dict['result'], " task_result_dict['email_class']: ", task_result_dict['email_class'], " task_result_dict['real_email_pk']: ", task_result_dict['real_email_pk'])
                        if task_result_dict['email_class'].lower() == 'authmodel.email':
                            query_emails_list.add(int(task_result_dict['real_email_pk']))
                        else:
                            query_spam_emails_list.add(int(task_result_dict['real_email_pk']))

            """ Если task.id закончились - выходим """
            if len(task_set) == 0:
                break

        """ Закрываем отсылку в самой рассылке """
        delivery.send_spam = True
        delivery.save()

        print('task_set: ', task_set, )

    except Delivery.DoesNotExist:
        return False

    return True, 'Start: {0} | End: {1}'.format(start, datetime.now())  # '__name__: {0}'.format(str(__name__))


@celery_app.task()
def processing_delivery(*args, **kwargs):

    delivery_pk = kwargs.get('delivery_pk')
    # logger.info(u'delivery_pk: {0}'.format(delivery_pk))
    delivery = Delivery.objects.get(pk=kwargs.get('delivery_pk'), )

    email_middle_delivery_pk = kwargs.get('email_middle_delivery_pk')
    # logger.info(u'email_middle_delivery_pk: {0}'.format(email_middle_delivery_pk))
    email_middle_delivery = EmailMiddleDelivery.objects.get(pk=kwargs.get('email_middle_delivery_pk'), )

    email_class = kwargs.get('email_class')
    # logger.info(u'email_class: {0}'.format(email_class))

    email_pk = kwargs.get('email_pk')
    # logger.info(u'email_pk: {0}'.format(email_pk))

    real_email = get_email(
        email_class=kwargs.get('email_class'),
        pk=kwargs.get('email_pk'), )

    email_for = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                                                now_email=real_email, )

    mail_account = get_mail_account()  # pk=1, )  # subscribe@keksik.com.ua
    if mail_account:
        msg = create_msg(delivery=delivery, mail_account=mail_account, email=email_for, test=False, )

        result = send(delivery=delivery, mail_account=mail_account, email=email_for, msg=msg)
    else:
        result = False

    if result:
        logger.info(
            'function processing_delivery(): datetime.now() {0}, delivery_pk: {1}, email_middle_delivery_pk: {2}'
            .format(datetime.now(), delivery_pk, email_middle_delivery_pk, ), )
        logger.info(
            'function processing_delivery(): email_class: {0}, email_pk: {1}, real_email.email: {2}'
            .format(email_class, email_pk, real_email.email))
        sleep(31)
        # sleep(17)
        return dict(result=result, )
    else:
        email_for.delete()
        return dict(result=result, email_class=email_class, real_email_pk=real_email.pk, )


@celery_app.task()
def get_mail_imap(*args, **kwargs):
    mail_account = get_mail_account(smtp=False, imap=True, )

    box = IMAP4_SSL(host=mail_account.server.server_imap,
                    port=mail_account.server.port_imap, )

    box.login(user=mail_account.username,
              password=mail_account.password, )

    box.select(mailbox='inbox', )

    result, all_msg_nums = box.search(None, 'ALL')

    result_msg_nums = set()

    if result == 'OK':

        msg_nums = set()

        for msg_num in all_msg_nums[0].split():

            result, fetch = box.fetch(message_set=msg_num,
                                      message_parts='(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])', )

            if result == 'OK':
                parse_msg = email.message_from_string(fetch[0][1])
                subj, error = str_conv(parse_msg['Subject'])

                if error:
                    logger.info(
                        u'Error in msg id: {0} | From: {1} | Date: {2} | datetime.now() {3} --> Subject: {4}'
                        .format(msg_num, parse_msg['From'], parse_msg['Date'], datetime.now(), parse_msg['Subject'], ))

                else:
                    try:
                        logger.info(
                            u'Info msg id: {0} | From: {1} | Date: {2} | datetime.now() {3} --> Subject: {4}'
                            .format(msg_num, parse_msg['From'], parse_msg['Date'],
                                    datetime.now(), parse_msg['Subject'], ))
                    except UnicodeDecodeError:
                        logger.info(
                            u'Info msg id: {0} | From: {1} | Date: {2} | datetime.now() {3}'
                            .format(msg_num, parse_msg['From'], parse_msg['Date'],
                                    datetime.now(), ))

                if subj == u'Недоставленное сообщение' \
                        and parse_msg['From'] == 'mailer-daemon@yandex.ru':

                    msg_nums.add(msg_num)

        logger.info(
            u'Info msg ids for work: {0}'
            .format(msg_nums, ))

        for msg_num in msg_nums:
            sleep(1)
            logger.info(
                u'Info msg id: {0} --> fetch from server for work'
                .format(msg_num, ))
            result, fetch = box.fetch(message_set=msg_num,
                                      message_parts='(RFC822)', )
            logger.info(
                u'Info fecth msg id: {0} result --> {1}'
                .format(msg_num, result ))
            if result == 'OK':
                parse_msg = email.message_from_string(fetch[0][1])

                email_message_id = parse_msg['Message-Id']
                email_from = parse_msg['From']
                email_to = parse_msg['To']
                subj, error = str_conv(parse_msg['Subject'])

                body = ''
                if parse_msg.is_multipart():
                    for part in parse_msg.walk():
                        ctype = part.get_content_type()
                        cdispo = str(part.get('Content-Disposition'))

                        # skip any text/plain (txt) attachments
                        if ctype == 'text/plain' and 'attachment' not in cdispo:
                            body = part.get_payload(decode=True)  # decode
                            break
                # not multipart - i.e. plain text, no attachments, keeping fingers crossed
                else:
                    body = parse_msg.get_payload(decode=True)

                list_lines = body.split('\r\n')
                for line_num, line in enumerate(list_lines):

                    if ('host' in line and 'said:' in line) \
                            or ('host' in line and 'said:' in list_lines[line_num + 1]):

                        i = 1
                        while True:
                            try:
                                line = ' '.join((line.strip(), list_lines[line_num + i].strip()))
                                i += 1
                            except IndexError:
                                break

                        if any((key in line and value in line) for key, value in reason550.iteritems()):

                            email_str = line.split('>')[0].strip('<')
                            email_obj = get_email_by_str(email=email_str, )

                            if email_obj:
                                email_obj.error550 = True
                                email_obj.error550_date = datetime.today()
                                email_obj.save()

                            raw_email_obj = RawEmail.objects.create(
                                account=mail_account,
                                message_id_header=email_message_id,
                                from_header=email_from,
                                to_header=email_to,
                                subject_header=subj,
                                raw_email=fetch[0][1],
                            )

                            if email_obj and raw_email_obj:
                                box.store(msg_num, '+FLAGS', '\\Deleted')
                                result_msg_nums.add(msg_num, )
                            else:
                                box.store(msg_num, '-FLAGS', '\\Seen')
    box.close()
    box.logout()
    return True, "Id's message deleted from server {0}".format(result_msg_nums, ), datetime.now()


@celery_app.task(run_every=timedelta(seconds=1))
def test():
    print('All work!!!')
    logger.info(u'message: datetime.now() {0}'.format(datetime.now()))
    # std_logger.info(u'message: datetime.now() {0}'.format(datetime.now()))
    # debug_log.info(u'message: {0}, datetime: {1}'.format('All Work', datetime.now()))
    return True, datetime.now()


import socket
import sockschain as socks
from random import randrange


@celery_app.task()
def processing_delivery_through_socks(*args, **kwargs):

    # message_pk = kwargs.get('message_pk')
    # logger.info(u'delivery_pk: {0}'.format(delivery_pk))
    message = model_Message.objects.get(pk=kwargs.get('message_pk'), )

    proxy_servers = models_socks.ProxyServer.objects.filter(Q(socks4=True) | Q(socks5=True), ).order_by('-socks4_pos', '-socks5_pos', )
    socket.setdefaulttimeout(10)
    s = socks.socksocket()
    type_socks = 4

    for n, serv in enumerate(proxy_servers):
        print('n: ', n, ' from: ', len(proxy_servers))
        if serv.socks4 and serv.socks5:
            type_socks = randrange(start=4, stop=5)
            print('randrange: type_sock: ', type_socks)
        if serv.socks4 or type_socks == 4:
            type_socks = socks.PROXY_TYPE_SOCKS4
        elif serv.socks5 or type_socks == 5:
            type_socks = socks.PROXY_TYPE_SOCKS5
        s.setproxy(type_socks, serv.host, serv.port)
        print('type: ', type_socks, 'serv.host: ', serv.host, 'serv.port: ', serv.port, ' : ', serv.socks4_pos, ' : ', serv.socks5_pos)

        for preference, smtp_serv in get_MXes(message.email.domain).iteritems():
            try:
                s.connect((smtp_serv, 25))
            except socket.error as e:
                print('Exception(socket.error): ', e)
                serv.dec_pos(type_socks)
                if socket.error.errno == 110:
                    serv.dec_pos(type_socks, int_dec=10)
                break
            except socks.GeneralProxyError as e:
                print('Exception(socks.GeneralProxyError): ', e)
                serv.dec_pos(type_socks)
                break
            except socks.Socks4Error as e:
                print('Exception(socks.Socks4Error): ', e)
                serv.dec_pos(type_socks)
                break
            except socks.Socks5Error as e:
                print('Exception(socks.Socks5Error): ', e)
                serv.dec_pos(type_socks)
                break


            print('smtp_serv: ', smtp_serv, 'port: ', 25)

            recv = s.recv(1024)
            print("Message after connection request:" + recv.decode())

            if recv[:3] != '220':
                print('220 reply not received from server.')
                break
            else:
                serv.inc_pos(type_socks, )

            heloCommand = 'HELO proxy.keksik.com.ua\r\n'
            s.send(heloCommand.encode())
            recv1 = s.recv(1024)
            print("Message after HeLO command:" + recv1.decode())

            if recv1[:3] != '250':
                print('250 reply not received from server.')
                break
            else:
                serv.inc_pos(type_socks, )

            mailFrom = "MAIL FROM:<alex.starov@gmail.com>\r\n"
            s.send(mailFrom.encode())
            recv2 = s.recv(1024)
            print("After MAIL FROM command: " + recv2.decode())

            if recv2[:3] != '250':
                print('250 reply not received from server.')
                break
            else:
                serv.inc_pos(type_socks, )

            rcptTo = "RCPT TO:<gserg@mail333.com>\r\n"

            s.send(rcptTo.encode())
            recv3 = s.recv(1024)
            print("After RCPT TO command: " + recv3.decode())

            if recv3[:3] != '250':
                print('250 reply not received from server.')
                break
            else:
                serv.inc_pos(type_socks, )

            data = "DATA\r\n"
            s.send(data.encode())
            recv4 = s.recv(1024)
            print("After DATA command: " + recv4.decode())

            msg = 'test - TEST - test\r\n.\r\n'
            s.send(msg.encode())

            recv_msg = s.recv(1024)
            print("Response after sending message body:" + recv_msg.decode())

            if recv_msg[:3] != '250':
                print('250 reply not received from server.')
                break
            else:
                serv.inc_pos(type_socks, 100)

            quit = "QUIT\r\n"
            s.send(quit.encode())
            recv5 = s.recv(1024)
            print(recv5.decode())
            s.close()


def get_MXes(domain, ):
    answers = dns.resolver.query(domain, 'MX')
    MX_dict = {rdata.preference: rdata.exchange.to_text().rstrip('.') for rdata in answers}
    # for rdata in answers:
    #     print('has preference: ', rdata.preference, ' Host: ', rdata.exchange, )
    return OrderedDict(sorted(MX_dict.items()))


@celery_app.task()
def socks_server_test(*args, **kwargs):

    host = kwargs.get('host')
    port = int(kwargs.get('port'))
    socks4 = kwargs.get('socks4', False)
    socks5 = kwargs.get('socks5', False)

    types_socks = set(); types_socks.add(socks.PROXY_TYPE_SOCKS4, socks.PROXY_TYPE_SOCKS5, )
    if socks4 and not socks5:
        types_socks = set(socks.PROXY_TYPE_SOCKS4, )
    elif not socks4 and socks5:
        types_socks = set(socks.PROXY_TYPE_SOCKS5, )

    socket.setdefaulttimeout(10)
    s = socks.socksocket()
    connect = False
    first_type_socks, second_type_socks = None, None

    for type_socks in types_socks:
        s.setproxy(type_socks, host, port)

        try:
            s.connect(('smtp.yandex.ru', 25))
            recv = s.recv(1024)
            print("Message after connection request:" + recv.decode())

            if recv[:3] != '220':
                print('220 reply not received from server.')
                continue

            s.send('HELO proxy.keksik.com.ua\r\n'.encode())
            recv = s.recv(1024); print("Message after HeLO command:" + recv.decode())

            if recv[:3] != '250':
                print('250 reply not received from server.')

            connect = True

            if not first_type_socks and not second_type_socks:
                first_type_socks = type_socks
            elif first_type_socks and not second_type_socks:
                second_type_socks = type_socks

            print('first_type_socks: ', first_type_socks, ' second_type_socks: ', second_type_socks, )

            quit = "QUIT\r\n"
            s.send(quit.encode())
            print(s.recv(1024).decode())
            s.close()

        except socket.error as e:
            print('Exception(socket.error): ', e)
            continue

        except socks.GeneralProxyError as e:
            print('Exception(socks.GeneralProxyError): ', e)
            continue

        except (socks.Socks4Error, socks.Socks5Error) as e:
            print('Exception(socks.Socks4Error or socks.Socks5Error): ', e)
            continue

    if connect:
        try:
            pr_serv = models_socks.ProxyServer.objects.get(host=host)
        except models_socks.ProxyServer.DoesNotExist:
            pr_serv = models_socks.ProxyServer(from_whence=3)
            pr_serv.host = host
            pr_serv.port = port

            if first_type_socks == socks.PROXY_TYPE_SOCKS4\
                    or second_type_socks == socks.PROXY_TYPE_SOCKS4:
                pr_serv.socks4 = True
            if first_type_socks == socks.PROXY_TYPE_SOCKS5\
                    or second_type_socks == socks.PROXY_TYPE_SOCKS5:
                pr_serv.socks5 = True
            pr_serv.save()

        except models_socks.ProxyServer.MultipleObjectsReturned:
            pr_serv = models_socks.ProxyServer.objects.filter(host=host)
            pr_serv[1].delete()
            pr_serv = pr_serv[0]

        print('pr_serv: ', pr_serv, ' host: ', host, ' port: ', port, ' OK')

    return connect
