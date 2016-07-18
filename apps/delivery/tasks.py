# -*- coding: utf-8 -*-
from proj.celery import celery_app
from datetime import datetime, timedelta
from celery.utils.log import get_task_logger
from time import sleep

from django.db.models import Q
from smtplib import SMTPSenderRefused, SMTPDataError

import email
from imaplib import IMAP4_SSL

from apps.authModel.models import Email
from .models import Delivery, EmailMiddleDelivery, EmailForDelivery, RawEmail
from .utils import get_mail_account, get_email, create_msg, connect, send_msg, str_conv, get_email_by_str

__author__ = 'AlexStarov'

logger = get_task_logger(__name__)

reason550 = {'google.com': 'said: 550-5.1.1 The email account that you tried to reach does not exist.',
             'mail.ru': 'said: 550 Message was not accepted -- invalid mailbox.',
             'ukr.net': 'said: 550-Message for',
             'i.ua': 'said: 550 Mailbox is frozen.',
             'bigmir.net': 'said: 550 Mailbox is frozen.',


             'dalgakiran.com.ua': 'said: 550 5.2.1 Mailbox unavailable.',
             'cook-time.com': 'said: 550 No Such User Here',
             'wr0.ru': 'said: 554 5.7.1',
             }


def send(delivery, mail_account, email, msg):
    try:
        connection = connect(mail_account=mail_account, fail_silently=False, )
        send_msg(connection=connection, mail_account=mail_account, email=email, msg=msg, )
    except SMTPSenderRefused as e:
        print('SMTPSenderRefused: ', e)
    except SMTPDataError as e:
        print('SMTPDataError: ', e)
    except Exception as e:
        print('Exception: ', e)
        if "(554, '5.7.1 Message rejected under suspicion of SPAM; http://help.yandex.ru/mail/spam/sending-limits.xml" in e:
            print('SPAM Bloked E-Mail: ', mail_account, ' NOW !!!!!!!!!!!!!!!!!!!!!!!')
            from datetime import datetime
            mail_account.is_auto_active = False
            mail_account.auto_active_datetime = datetime.now()
            mail_account.save()
        connection = connect(mail_account=mail_account, fail_silently=True, )
        msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, exception=e, test=True, )
        send_msg(connection=connection, mail_account=mail_account, email=email, msg=msg, )


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

        real_email = get_email(delivery=delivery, email_class=Email, pk=6, )  # pk=2836, )  # pk=6, ) subscribe@keksik.com.ua
        email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                                                now_email=real_email,
                                                email=real_email, )
        mail_account = get_mail_account(pk=1, )  # subscribe@keksik.com.ua
        msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, test=True, )
        """ Посылаем письмо - subscribe@keksik.com.ua """
        send(delivery=delivery, mail_account=mail_account, email=email, msg=msg)

        """ Посылаем письмо - check-auth2@verifier.port25.com """
        real_email = get_email(delivery=delivery, email_class=Email, pk=7, )  #pk=3263, )  # pk=7, ) check-auth2@verifier.port25.com
        email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                                                now_email=real_email,
                                                email=real_email, )
        send(delivery=delivery, mail_account=mail_account, email=email, msg=msg)

    except Delivery.DoesNotExist:
        return False

    return True, datetime.now(), '__name__: {0}'.format(str(__name__))


from celery.utils import uuid


@celery_app.task()
def processing_delivery_real(*args, **kwargs):
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
                                                                   delivery_send=True, )

        try:
            query_emails = Email.objects\
                .filter(bad_email=False, error550=False, )\
                .order_by('?')
            query_emails_list = set(obj.pk for obj in query_emails)

        except Email.DoesNotExist:
            return False, datetime.now()

        task_set = set()

        while True:
            if len(query_emails_list) > 0 and len(query_emails) > 0:
                real_email, query_emails_list, query_emails = get_email(
                    delivery=delivery,
                    queryset_list=query_emails_list,
                    queryset=query_emails,
                )

                if real_email is False:
                    break

                task = processing_delivery.apply_async(
                    queue='delivery_send',
                    kwargs={'delivery_pk': delivery.pk,
                            'email_middle_delivery_pk': email_middle_delivery.pk,
                            'email_class': Email.__name__,
                            'email_pk': real_email.pk},
                    task_id='celery-task-id-{0}'.format(uuid(), ),
                )

                logger.info(u'Task.id : {0} --> Email.__name__: {1} --> email: {2}'
                    .format(task.id, Email.__name__, email.email, ), )

                task_set.add(task.id, )

            else:
                break

        """ Закрываем отсылку в самой рассылке """
        delivery.send = True
        delivery.save()

        print 'task_set: ', task_set

    except Delivery.DoesNotExist:
            delivery = False

    return True, datetime.now()  # '__name__: {0}'.format(str(__name__))


@celery_app.task()
def processing_delivery(*args, **kwargs):

    delivery_pk = kwargs.get('delivery_pk')
    logger.info(u'delivery_pk: {0}'.format(delivery_pk))
    delivery = Delivery.objects.get(pk=delivery_pk, )

    email_middle_delivery_pk = kwargs.get('email_middle_delivery_pk')
    logger.info(u'email_middle_delivery_pk: {0}'.format(email_middle_delivery_pk))
    email_middle_delivery = EmailMiddleDelivery.objects.get(pk=email_middle_delivery_pk, )

    email_class = kwargs.get('email_class')
    logger.info(u'email_class: {0}'.format(email_class))

    email_pk = kwargs.get('email_pk')
    logger.info(u'email_pk: {0}'.format(email_pk))

    real_email = get_email(delivery=delivery, email_class=email_class, pk=email_pk, )

    email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                                            now_email=real_email,
                                            email=real_email, )

    mail_account = get_mail_account(pk=1, )  # subscribe@keksik.com.ua
    msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, test=False, )

    send(delivery=delivery, mail_account=mail_account, email=email, msg=msg)

    logger.info(u'message: datetime.now() {0}, delivery_pk: {1}'.format(datetime.now(), delivery_pk))
    sleep(30)
    return '__name__: {0}'.format(str(__name__))


@celery_app.task()
def get_mail_imap(*args, **kwargs):
    mail_account = get_mail_account(smtp=False, imap=True, )

    box = IMAP4_SSL(host=mail_account.server.server_imap,
                    port=mail_account.server.port_imap, )

    box.login(user=mail_account.username,
              password=mail_account.password, )

    box.select(mailbox='inbox', )

    result, all_msg_nums = box.search(None, 'ALL')

    if result == 'OK':

        msg_nums = set()

        for msg_num in all_msg_nums[0].split():

            result, fetch = box.fetch(message_set=msg_num,
                                      message_parts='(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])', )

            if result == 'OK':
                parse_msg = email.message_from_string(fetch[0][1])
                subj, error = str_conv(parse_msg['Subject'])

                if error:
                    logger.info(u'Error in msg id: {0} | From: {1} | Date: {2} | datetime.now() {3} --> Subject: {4}'
                        .format(msg_num, parse_msg['From'], parse_msg['Date'], datetime.now(), parse_msg['Subject']))

                if str_conv(parse_msg['Subject']) == u'Недоставленное сообщение' \
                        and parse_msg['From'] == 'mailer-daemon@yandex.ru':

                    msg_nums.add(msg_num)

        for msg_num in msg_nums:
            sleep(5)
            result, fetch = box.fetch(message_set=msg_num,
                                      message_parts='(RFC822)', )
            if result == 'OK':
                parse_msg = email.message_from_string(fetch[0][1])

                email_message_id = parse_msg['Message-Id']
                email_from = parse_msg['From']
                email_to = parse_msg['To']
                subj = str_conv(parse_msg['Subject'])

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
                            else:
                                box.store(msg_num, '-FLAGS', '\\Seen')
    box.close()
    box.logout()
    return True, datetime.now()


@celery_app.task(run_every=timedelta(seconds=1))
def test():
    print('All work!!!')
    logger.info(u'message: datetime.now() {0}'.format(datetime.now()))
    # std_logger.info(u'message: datetime.now() {0}'.format(datetime.now()))
    # debug_log.info(u'message: {0}, datetime: {1}'.format('All Work', datetime.now()))
    return True, datetime.now()

