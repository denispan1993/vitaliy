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


def Mail_Account():
    from apps.delivery.models import MailAccount
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
        return True
    else:
        return True

import sys
from apps.authModel.models import Email
from apps.delivery.models import SpamEmail


def get_email(delivery, email_class=None, ):
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
            email = email_class.objects.get(pk=random_email_pk, bad_email=False, )
        except email_class.DoesNotExist:
            pass
        else:
            try:
                EmailForDelivery.objects.get(delivery__delivery=delivery,
                                             content_type=email.content_type,
                                             object_id=email.pk, )
            except EmailForDelivery.DoesNotExist:
                print '\n'
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
    elif isinstance(last_email, SpamEmail, ):
        random_list = random_SpamEmail
    while True:
        random_email_pk = randrange(1, last_email.pk, )
        if random_email_pk not in random_list:
            random_list.append(random_email_pk, )
            print '\n'
            return random_email_pk
        else:
            print random_email_pk, ', ',
