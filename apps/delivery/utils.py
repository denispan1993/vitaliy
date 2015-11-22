# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'


def parsing(value, key, ):
    from re import split
    values = split("{{ id }}*", value, )
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
    return value


def Mail_Account(pk=False, ):
    from apps.delivery.models import MailAccount
    if pk:
        try:
            pk = int(pk, )
        except ValueError:
            return False
        else:
            try:
                mail_account = MailAccount.objects.get(pk=pk, )
            except MailAccount.DoesNotExist:
                return False
            else:
                return mail_account
    mail_accounts = MailAccount.objects.filter(is_active=True, ).order_by('?')

    # last_mail_accounts = MailAccount.objects.latest('pk', )
    len_mail_accounts = len(mail_accounts, )
    from random import randrange
    loop = True
    while loop:
        mail_account_id = randrange(1, len_mail_accounts, )
        try:
            mail_account = mail_accounts[mail_account_id]
        except IndexError:
            pass
        else:
            if mail_account.is_auto_active:
                print 'MailAccount: ', mail_account
                return mail_account
            else:
                from datetime import datetime, timedelta
                datetimedelta = mail_account.auto_active_datetime + timedelta(days=1, hours=1, minutes=30, )
                if datetimedelta < datetime.now():
                    mail_account.is_auto_active = True
                    mail_account.save()
                    print 'MailAccount: ', mail_account
                    return mail_account


def Backend(mail_account=None, ):
    if mail_account is None:
        mail_account = Mail_Account()
    from django.core.mail import get_connection

    if mail_account.server.use_ssl and not mail_account.server.use_tls:
        backend='apps.delivery.backends.smtp.EmailBackend',
    elif not mail_account.server.use_ssl and mail_account.server.use_tls:
        backend = 'django.core.mail.backends.smtp.EmailBackend'
    else:
        return None
    backend = get_connection(backend=backend,
                             host=mail_account.server.server,
                             port=mail_account.server.port,
                             username=mail_account.username,
                             password=mail_account.password,
                             use_tls=mail_account.server.use_tls,
                             fail_silently=False,
                             use_ssl=mail_account.server.use_ssl,
                             timeout=10, )

    return backend


def Test_Server_MX_from_email(email_string=None, resolver=None, ):
    try:
        domain = email_string.split('@', )[1]
    except IndexError:
        print 'Bad E-Mail: IndexError: ', email_string
        return False

    if resolver is None:
        import dns.resolver
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['192.168.1.100', ]

    from dns.resolver import NXDOMAIN, NoAnswer, NoNameservers
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

import sys
from apps.authModel.models import Email
from apps.delivery.models import SpamEmail


def get_email(delivery, email_class=None, pk=False, ):
    from apps.delivery.models import EmailForDelivery
    if email_class is None or (email_class != Email and email_class != SpamEmail):
        from apps.authModel.models import Email as email_class

    last_emails = email_class.objects.filter(bad_email=False, ).order_by('-id', )[:1]
    last_email = last_emails[0]
    loop =True
    while loop:
        # print '.',
        sys.stdout.flush()
        random_email_pk = random(last_email, )
        try:
            if pk:
                try:
                    pk = int(pk, )
                    print 'pk: ', pk
                except ValueError:
                    print 'pk: ', pk
                    return False
                else:
                    email = email_class.objects.get(pk=pk, )
            else:
                email = email_class.objects.get(pk=random_email_pk, bad_email=False, )
        except email_class.DoesNotExist:
            if pk:
                print 'pk DoesNotExit: ', pk
                return False
        else:
            if pk:
                return email
            try:
                EmailForDelivery.objects.get(delivery__delivery=delivery,
                                             content_type=email.content_type,
                                             object_id=email.pk, )
            except EmailForDelivery.DoesNotExist:
                # print '\n'
                return email
            except EmailForDelivery.MultipleObjectsReturned:
                emails_fordelivery = EmailForDelivery.objects.filter(delivery__delivery=delivery,
                                                                     content_type=email.content_type,
                                                                     object_id=email.pk, )
                i = 0
                for email in emails_fordelivery:
                    i += 1
                    print 'i: ', i, ' - ', email


from random import randrange
from apps.delivery import random_Email, random_SpamEmail


def random(last_email, ):
    if isinstance(last_email, Email, ):
        random_list = random_Email
        # print 'random_Email: ', random_list
    elif isinstance(last_email, SpamEmail, ):
        random_list = random_SpamEmail
        # print 'random_SpamEmail: ', random_list
    while True:
        random_email_pk = randrange(1, last_email.pk, )
        if random_email_pk not in random_list:
            random_list.append(random_email_pk, )
            print '\n'
            return random_email_pk
        else:
            print random_email_pk, ', ',
            sys.stdout.flush()

named = lambda email, name=False: ('%s <%s>' % email, name) if name else email


def create_msg(delivery, mail_account, email, test=False, ):
    from email import MIMEMultipart, MIMEText, MIMEImage

    msgRoot = MIMEMultipart('related', )
    msgRoot['Subject'] = 'test - %s' % delivery.subject if not test else delivery.subject
    msgRoot['From'] = named(mail_account.email, )
    msgRoot['To'] = named(email.now_email.email, )
    msgRoot.preamble = 'This is a multi-part message in MIME format.'
    msgAlternative = MIMEMultipart('alternative', )
    msgRoot.attach(msgAlternative, )

    charset = 'utf-8'
    from django.utils.html import strip_tags
    msgAlternative.attach(MIMEText(strip_tags(parsing(value=delivery.html,
                                                      key=email.key, ), ),
                                   'plain',
                                   _charset=charset), )
    msgAlternative.attach(MIMEText(parsing(value=delivery.html,
                                           key=email.key, ),
                                   'html',
                                   _charset=charset), )
    """ Привязываем картинки. """
    images = delivery.images
    for image in images:
        image_file = open(image.image.path, 'rb', )
        msg_image = MIMEImage(image_file.read(), )
        image_file.close()
        # msg_image.add_header('Content-Disposition', 'inline', filename=image.image.filename, )
        msg_image.add_header('Content-ID', '<%s>' % image.tag_name, )
        msgRoot.attach(msg_image)
    return msgRoot


def connect(mail_account=False, timeout=False, fail_silently=True, ):
    from smtplib import SMTP, SMTP_SSL, SMTPException
    connection_class = SMTP_SSL if mail_account.server.use_ssl and \
                                   not mail_account.server.use_tls else SMTP
    from django.core.mail.utils import DNS_NAME
    connection_params = {'local_hostname': DNS_NAME.get_fqdn()}
    if timeout:
        connection_params['timeout'] = timeout
    try:
        connection = connection_class(host=mail_account.server.server,
                                      port=mail_account.server.port,
                                      **connection_params)
        if not mail_account.server.use_ssl and mail_account.server.use_tls:
            connection.ehlo()
            connection.starttls()
            connection.ehlo()
        if mail_account.username and mail_account.password:
            connection.login(mail_account.username, mail_account.password, )
        return connection
    except SMTPException:
        if not fail_silently:
            raise


def send_msg(connection, mail_account, email, msg, ):
    connection.sendmail(from_addr=mail_account.email,
                        to_addrs=email.now_email.email,
                        msg=msg.as_string(), )
    connection.quit()
    return True
