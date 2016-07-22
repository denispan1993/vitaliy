# -*- coding: utf-8 -*-
from proj.celery import celery_app
from datetime import datetime, timedelta
from celery.utils.log import get_task_logger
from time import sleep

from django.db.models import Q

import email
from imaplib import IMAP4_SSL

from apps.authModel.models import Email
from .models import Delivery, EmailMiddleDelivery, EmailForDelivery, SpamEmail, RawEmail
from .utils import get_mail_account, get_email, create_msg, str_conv, get_email_by_str, send

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)

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
        email_middle_delivery = EmailMiddleDelivery.objects.create(delivery=delivery,
                                                                   delivery_test_send=True,
                                                                   delivery_send=False, )
        """ Закрываем отсылку теста в самой рассылке """
        delivery.send_test = True
        delivery.save()

        real_email = get_email(delivery=delivery, email_class=Email, pk=2836, )  # pk=6, ) subscribe@keksik.com.ua
        email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                                                now_email=real_email,
                                                email=real_email, )
        mail_account = get_mail_account(pk=1, )  # subscribe@keksik.com.ua
        msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, test=True, )
        """ Посылаем письмо - subscribe@keksik.com.ua """
        send(delivery=delivery, mail_account=mail_account, email=email, msg=msg)

        """ Посылаем письмо - check-auth2@verifier.port25.com """
        real_email = get_email(delivery=delivery, email_class=Email, pk=3263, )  # pk=7, ) check-auth2@verifier.port25.com
        email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                                                now_email=real_email,
                                                email=real_email, )
        send(delivery=delivery, mail_account=mail_account, email=email, msg=msg)

    except Delivery.DoesNotExist:
        return False

    return True, datetime.now(), '__name__: {0}'.format(str(__name__))


from celery.utils import uuid
from celery.result import AsyncResult


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
                sleep(3)

                task = AsyncResult(task_id, )
                if task.status == 'SUCCESS':

                    task_set.remove(task_id)

                    task_result_dict = task.result
                    print('REMOVE!!!!!!!!! --> ', 'task_id: ', task_id, 'task.status: ', task.status, 'task_result_dict: ', task_result_dict)

                    if task_result_dict['result'] is not True:
                        query_emails_list.add(task_result_dict['real_email_pk'])

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
        sleep(29)
        # sleep(17)
        return dict(result=result, )
    else:
        email_for.delete()
        return dict(result=result, real_email_pk=real_email.pk, )


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

