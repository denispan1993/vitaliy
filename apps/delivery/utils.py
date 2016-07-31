# -*- coding: utf-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from re import split

import copy
import re
import quopri
import base64
import sys
from django.core.mail import get_connection, EmailMultiAlternatives
from django.core.mail.utils import DNS_NAME
from django.db.models import Q
from django.db.models.loading import get_model
from django.utils.html import strip_tags
from smtplib import SMTP, SMTP_SSL, SMTPException, SMTPServerDisconnected, SMTPSenderRefused, SMTPDataError
from random import randrange, randint, choice
from datetime import datetime, timedelta
from time import mktime, sleep
from logging import getLogger
from email.utils import formataddr
from dns.resolver import Resolver, NXDOMAIN, NoAnswer, NoNameservers

from . import random_Email, random_SpamEmail
from apps.authModel.models import Email
from .models import MailAccount, EmailForDelivery, SpamEmail

__author__ = 'AlexStarov'

std_logger = getLogger(__name__)

"(554, '5.7.1 Message rejected under suspicion of SPAM; http://help.yandex.ru/mail/spam/sending-limits.xml",\
"5.7.1 Message rejected under suspicion of SPAM; https://ya.cc/0EgTP 1469197349-4HnTGIgAOk-MSwGPtbw"


def parsing(value, key, ):
    values = split("{{ id }}", value, )
    cycle = 1
    part_count = len(values, )
    if part_count > 1:
        value = ''
        for value_part in values:  # [::2]:  # перечисляем все куски с шагом 2
            if not part_count == cycle:
                value = '%s%s%s' % (value, value_part, key, )
            else:
                value = '%s%s' % (value, value_part, )
                break
            cycle += 1
    """ Перед возвращением тела письма, парсим его на предмет "[[разных|одинаковых]]" слов """
    return choice_str_in_tmpl(tmpl=value, )


def get_mail_account(pk=False, smtp=True, imap=False, pop3=False, ):
    if pk:
        try:
            pk = int(pk, )
            try:
                return MailAccount.objects.get(pk=pk, )
            except MailAccount.DoesNotExist:
                return False
        except (TypeError, ValueError):
            return False

    query = Q()
    if smtp:
        query &= Q(server__use_smtp=True, ) & Q(use_smtp=True, )
    if imap:
        query &= Q(server__use_imap=True, ) & Q(use_imap=True, )
    if pop3:
        query &= Q(server__use_pop3=True, ) & Q(use_pop3=True, )

    mail_accounts = MailAccount.objects.filter(query, ).order_by('?')

    len_mail_accounts = MailAccount.objects.values_list('pk', flat=True).filter(query, ).latest('id', )

    i = 0
    while True:
        mail_account_id = randrange(1, len_mail_accounts, )
        i += 1
        try:
            mail_account = mail_accounts[mail_account_id]

            if not smtp and (imap or pop3):
                print('MailAccount: ', mail_account)
                return mail_account

            if smtp and mail_account.is_auto_active:
                print('MailAccount: ', mail_account)
                return mail_account

            else:
                print('==============| ', 'MailAccount: ', mail_account, ' |================')
                aaa = timedelta(hours=2, )
                print('TimeDelta: timedelta(hours=2, ): ', aaa)
                bbb = mail_account.auto_active_datetime
                print('mail_account.auto_active_datetime: ', bbb)
                bbb = bbb.replace(tzinfo=None, )
                print('mail_account.auto_active_datetime.replace(tzinfo=None): ', bbb)
                bbb += aaa
                print('mail_account.auto_active_datetime.replace(tzinfo=None) + TimeDelta: ', bbb)
                ccc = datetime.now()
                print('datetime.now(): ', ccc)
                ccc = ccc.replace(tzinfo=None, )
                print('datetime.now().replace(tzinfo=None, ): ', ccc)
                print('===================================================================')
                """ Берем дататайм из базы,
                    убираем часовой пояс,
                    + 2 часа нашего часового пояса,
                    + смещение 1 день 1 час 30 минут """
                datetime_delta = mail_account.auto_active_datetime.\
                                     replace(tzinfo=None, )\
                                     + timedelta(hours=2, )\
                                     + timedelta(days=1, hours=1, minutes=30, )
                if datetime_delta < datetime.now():
                    mail_account.is_auto_active = True
                    mail_account.save()
                    print('MailAccount: ', mail_account)
                    return mail_account

        except IndexError:
            pass

        sleep(1)
        if i > 100:
            """ Если нету свободных почтовых аккаунтов,
                то ждем пол часа и выходим """
            sleep(1800, )
            return False


def Backend(mail_account=None, ):
    if mail_account is None:
        mail_account = get_mail_account()

    if mail_account.server.use_ssl and not mail_account.server.use_tls:
        backend='apps.delivery.backends.smtp.EmailBackend',
    elif not mail_account.server.use_ssl and mail_account.server.use_tls:
        backend = 'django.core.mail.backends.smtp.EmailBackend'
    else:
        return None
    backend = get_connection(backend=backend,
                             host=mail_account.server.server_smtp,
                             port=mail_account.server.port_smtp,
                             username=mail_account.username,
                             password=mail_account.password,
                             use_tls=mail_account.server.use_tls_smtp,
                             fail_silently=False,
                             use_ssl=mail_account.server.use_ssl_smtp,
                             timeout=10, )

    return backend


def Test_Server_MX_from_email(email_string=None, resolver=None, ):
    try:
        domain = email_string.split('@', )[1]
    except IndexError:
        print 'Bad E-Mail: IndexError: ', email_string
        return False

    if resolver is None:
        resolver = Resolver()
        resolver.nameservers = ['192.168.1.100', '192.168.5.100', ]

    try:
        resolver.query(domain, 'mx', )
    except NXDOMAIN:
        print 'Bad E-Mail: Domain: ', email_string
        return False
    except NoNameservers:
        print 'NoNameServers for Domain: ', email_string
        return False
    except NoAnswer:
        print 'NoAnswer for Domain: ', email_string
        return False
    else:
        return True


def get_email(delivery=False, email_class=False, pk=False, query=False, queryset_list=False, queryset=False, ):

    if isinstance(email_class, (str, unicode)):
        email_model = get_model(*email_class.split('.'))

    if isinstance(email_class, (Email, SpamEmail)):
        email_model = email_class

    if isinstance(email_class, bool):
        from apps.authModel.models import Email as email_model

    if pk:
        try:
            pk = int(pk, )
            try:
                return email_model.objects.get(pk=pk, )
            except email_model.DoesNotExist:
                return False

        except (TypeError, ValueError):
            return False

    if not query:
        query = Q(bad_email=False, error550=False, )

    last_email = email_model.objects.filter(query, ).latest('id', )

    while True:
        sys.stdout.flush()
        try:

            if isinstance(queryset_list, bool) and queryset_list is False:
                random_pk = rand(last_email, query)
            elif queryset_list and len(queryset_list, ) > 0:
                random_pk = queryset_list.pop()
            elif len(queryset_list, ) == 0:
                return False, queryset_list, queryset

            if not random_pk:
                """ Если закончились цифры для перебора в рандоме - то выходим """
                return False

            if isinstance(queryset_list, bool) and queryset_list is False:
                real_email = email_model.objects.get(Q(pk=random_pk) & query)
            else:
                try:
                    real_email = queryset.get(pk=random_pk); queryset = queryset.exclude(pk=random_pk)
                except email_model.DoesNotExist:
                    real_email = email_model.objects.get(Q(pk=random_pk) & query)

            try:
                EmailForDelivery.objects.get(delivery__delivery=delivery,
                                             content_type=real_email.content_type,
                                             object_id=real_email.pk, )
            except EmailForDelivery.DoesNotExist:

                if not isinstance(queryset_list, set):
                    return real_email
                else:
                    return real_email, queryset_list, queryset

            except EmailForDelivery.MultipleObjectsReturned:
                emails_for_delivery = EmailForDelivery.objects.filter(delivery__delivery=delivery,
                                                                      content_type=real_email.content_type,
                                                                      object_id=real_email.pk, )
                i = 1
                for real_email in emails_for_delivery:
                    print('i: ', i, ' - ', real_email); i += 1

        except email_model.DoesNotExist:
            if queryset_list and queryset:
                queryset_list = queryset_list.remove(random_pk, )
                queryset = queryset.exclude(pk=random_pk)


def get_email_by_str(email, ):

    try:
        return Email.objects.get(email=email, )
    except Email.DoesNotExist:
        try:
            return SpamEmail.objects.get(email=email, )
        except SpamEmail.DoesNotExist:
            return False


def rand(last_email, query=False):
    if not query:
        query = Q(bad_email=False, error550=False,)

    if isinstance(last_email, Email, ):
        random_list = random_Email
        count_emails = Email.objects.filter(query).count()
    elif isinstance(last_email, SpamEmail, ):
        random_list = random_SpamEmail
        count_emails = SpamEmail.objects.filter(query).count()

    random_false = False
    while True:

        """ Если длина листа больше чем количество емыйлов в базе - то выходим """
        if len(random_list, ) - 5 >= count_emails:
            return False

        random_email_pk = randrange(1, last_email.pk, )
        """ Если такого pk еще нету в листе, то добавляем и выходим - возвращая pk """
        if random_email_pk not in random_list:
            random_list.append(random_email_pk, )
            if random_false:
                print('\n')
            return random_email_pk

        else:
            random_false = True
            print(random_email_pk, ', ')
            sys.stdout.flush()


named = lambda email, name=False: ('%s <%s>' % email, name) if name else email


def create_msg(delivery, mail_account, email, exception=False, test=False, ):

    """ did - Delivery id """
    did = get_div(delivery=delivery)
    headers = {'X-Delivery-id': did}
    """ eid - Email id """
    eid = get_eid(email=email.now_email)
    headers['X-Email-id'] = get_eid(email=email.now_email)
    """ mid - Message id """
    headers['X-Message-id'] = get_mid(div=did, eid=eid)
    """ Reply-To + Return-Path """
    headers['Return-Path'] = mail_account.get_return_path_subscribe
    headers['Reply-To'] = mail_account.get_return_path_subscribe

    message_kwargs = {
        'subject': u'test - {}'.format(delivery.subject) if test else delivery.subject,
        'body': strip_tags(parsing(value=delivery.html, key=email.key, ), ),
        'headers': headers,
        'from_email': formataddr((u'Интернет магаизн Keksik', mail_account.email)),
        'to': [mail_account.email if exception else email.now_email.email, ],
    }

    message = EmailMultiAlternatives(**message_kwargs)
    message.attach_alternative(parsing(value=delivery.html, key=email.key, ), 'text/html')

    return message.message()
    #for attachment in (self.attachments or []):
    #    path = os.path.join(
    #        settings.MEDIA_ROOT, attachment['filepath'])
    #    with open(path, 'r') as f:
    #        message.attach(
    #                                                                                                                                                                                                                                                                 attachment['filename'], f.read(),
    #            attachment['mimetype'])
    #    os.remove(path)

#    return message.message().as_bytes()

    # msgRoot = MIMEMultipart('related', )

    # msgRoot['Subject'] = 'test - {}'.format(delivery.subject) if test else delivery.subject
    # msgRoot['From'] = named(mail_account.email, )
    # if exception:
    #     to = mail_account.email
    # else:
    #     to = named(email.now_email.email, )
    # msgRoot['To'] = to
    # msgRoot.preamble = 'This is a multi-part message in MIME format.'
    # msgAlternative = MIMEMultipart('alternative', )
    # msgRoot.attach(msgAlternative, )

    # charset = 'utf-8'
    #if exception:
    #    msgAlternative.attach(MIMEText('%s\nFrom: %s\nTo: %s' % (exception, mail_account, email, ),
    #                                   'plain',
    #                                   _charset=charset), )
    #else:
    #    from django.utils.html import strip_tags
    #    msgAlternative.attach(MIMEText(strip_tags(parsing(value=delivery.html,
    #                                                      key=email.key, ), ),
    #                                   'plain',
    #                                   _charset=charset), )
    #    msgAlternative.attach(MIMEText(parsing(value=delivery.html,
    #                                           key=email.key, ),
    #                                   'html',
    #                                   _charset=charset), )
#    """ Привязываем картинки. """
#    if not exception:
#        images = delivery.images
#        for image in images:
#            image_file = open(image.image.path, 'rb', )
#            msg_image = MIMEImage(image_file.read(), )
#            image_file.close()
#            # msg_image.add_header('Content-Disposition', 'inline', filename=image.image.filename, )
#            msg_image.add_header('Content-ID', '<%s>' % image.tag_name, )
#            msgRoot.attach(msg_image)
#    return msgRoot


def connect(mail_account=False, timeout=False, fail_silently=True, ):
    if not mail_account:
        mail_account = get_mail_account()

    connection_class = SMTP_SSL if mail_account.server.use_ssl_smtp and \
                                   not mail_account.server.use_tls_smtp else SMTP
    connection_params = {'local_hostname': DNS_NAME.get_fqdn()}

    if timeout:
        connection_params['timeout'] = timeout
    try:
        connection = connection_class(host=mail_account.server.server_smtp,
                                      port=mail_account.server.port_smtp,
                                      **connection_params)
        if not mail_account.server.use_ssl_smtp and mail_account.server.use_tls_smtp:
            connection.ehlo()
            connection.starttls()
            connection.ehlo()
        if mail_account.username and mail_account.password:
            connection.login(mail_account.username, mail_account.password, )
        return connection
    except (SMTPException, SMTPServerDisconnected):
        if not fail_silently:
            raise
        else:
            return False


def send_msg(connection, mail_account, email, msg, execption=False, ):
    if execption:
        to = mail_account.email
    else:
        to = email.now_email.email
    connection.sendmail(from_addr=mail_account.email,
                        to_addrs=to,
                        msg=msg.as_string(), )
    connection.quit()
    return True


def send(delivery, mail_account, email, msg):
    try:
        connection = connect(mail_account=mail_account, fail_silently=False, )
        send_msg(connection=connection, mail_account=mail_account, email=email, msg=msg, )

        return True

    except SMTPSenderRefused as e:
        print('SMTPSenderRefused: ', e)

    except SMTPDataError as e:
        print('SMTPDataError: ', e, ' messages: ', e.message, ' smtp_code: ', e.smtp_code, 'smtp_error: ', e.smtp_error, ' args: ', e.args)

        if e.smtp_code == 554 and\
                "5.7.1 Message rejected under suspicion of SPAM; https://ya.cc/" in e.smtp_error:
            print('SPAM Bloked E-Mail: ', mail_account, ' NOW !!!!!!!!!!!!!!!!!!!!!!!')
            mail_account.is_auto_active = False
            mail_account.auto_active_datetime = datetime.now()
            mail_account.save()

            connection = connect(mail_account=mail_account, fail_silently=True, )
            msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, exception=e, test=True, )
            send_msg(connection=connection, mail_account=mail_account, email=email, msg=msg, )

    except Exception as e:
        print('Exception: ', e)

    return False


def sleep_now(time, email, i, ):
    print('i: ', i, 'Pk: ', email.now_email.pk, ' - ', email.now_email.email)
    time_now = randrange(9, 33, )
    time += time_now
    print('Time_now: ', time_now, ' average time: ', time/i)
    for n in range(1, time_now, ):
        print('.',)
        sys.stdout.flush()
        sleep(1, )
    print('\n')
    return time


def get_div(delivery):
    """ div - Delivery id """
    return '{0:04d}-{0:02d}'.format(delivery.pk, delivery.type, )


def get_eid(email):
    """ eid - Email id
        1 - Нормальные E-Mail
        2 - Spam E-Mail """
    if email.__class__.__name__ == 'Email':
        email_type = 1
    elif email.__class__.__name__ == 'SpamEmail':
        email_type = 2
    else:
        email_type = 0

    return '{0:02d}-{1:07d}'.format(email_type, email.pk, )


def get_mid(div, eid):
    """ mid - Message id """
    return '{0}-{1}-{2:011x}-{3:x}'\
        .format(div, eid, int(mktime(datetime.now().timetuple())), randint(0, 10000000), )


def str_encode(string='', encoding=None, errors='strict'):
    # If errors is 'strict' (the default), a ValueError is raised on errors,
    #  while a value of 'ignore' causes errors to be silently ignored, and a
    #  value of 'replace' causes the official Unicode replacement character,
    #  U+FFFD, to be used to replace input characters which cannot be decoded.
    return unicode(string, encoding, errors)


def str_decode(value='', encoding=None, errors='strict'):
    return value.decode(encoding, errors)


def str_conv(str, ):
    error = False

    if not str:
        return str, error

    values = str.split('\n')
    value_results = []

    for value in values:
        match = re.search(r'=\?((?:\w|-)+)\?(Q|q|B|b)\?(.+)\?=', value)
        if match:
            encoding, type_, code = match.groups()
            if type_.upper() == 'Q':
                value = quopri.decodestring(code)
            elif type_.upper() == 'B':
                value = base64.decodestring(code)
            try:
                value = str_encode(string=value, encoding=encoding, )
            except UnicodeDecodeError:
                value = str_encode(string=value, encoding=encoding, errors='replace', )
                error = True
            value_results.append(value)

    if len(value_results) > 0:
        return ''.join(value_results), error

    return str, error

tokenizer_replacement = re.compile('(\[[\[a-z|A-Z0-9\-\_\.]+\]])', re.MULTILINE)
# ccc('aaa [[bbb|111]] ccc [[ddd|222]] eee [[fff|333|444|555|666]] ggg')


def choice_str_in_tmpl(tmpl, ):
    three = re.split(tokenizer_replacement, tmpl)

    nodes = {}
    for pos, block in enumerate(three):
        if block.startswith('[[') and block.endswith(']]'):
            keys = block.strip('[[]]').split('|')

            value = keys[randrange(start=0, stop=len(keys))]

            if pos not in nodes:
                nodes[pos] = value

    three = copy.copy(three)
    for pos, value in nodes.iteritems():

        three[pos] = value

    return ''.join(three)


tokenizer = re.compile('(\{{[a-zA-Z0-9\-\_\.]+\}})', re.MULTILINE)
#bbb('aaa {{aaa1}} ccc {{bbb2}} eee {{ccc3}} ggg', {'aaa1': '1aaa', 'bbb2': 'bb2b', 'ccc3': 'ccc333ccc', })


def bbb(tmpl, context={}, ):
    three = re.split(tokenizer, tmpl)

    nodes = {}
    for pos, block in enumerate(three):
        if block.startswith('{{') and block.endswith('}}'):
            key = block.strip('{{}}')
            if key not in nodes:
                nodes[key] = []
            nodes[key].append(pos)
    keys = nodes.keys()
    three = copy.copy(three)
    for key, value in context.iteritems():
        if key in keys:
            for pos in nodes[key]:
                three[pos] = value

    print '!!!!!!!!!!', ''.join(three)
