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


def Mail_Account(mail_accounts=None, ):
    if mail_accounts is None:
        from apps.delivery.models import MailAccount
        mail_accounts = MailAccount.objects.filter(is_active=True, ).values_list().order_by('?')
    else:
        mail_accounts = list(mail_accounts, )

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


def Test_Server_MX(server_string=None, resolver=None, ):
    if server_string is None:
        return False

    if resolver is None:
        import dns.resolver
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['192.168.1.100', ]

    from dns.resolver import NXDOMAIN, NoAnswer
    try:
        resolver.query(server_string, 'mx', )
    except NXDOMAIN:
        print 'Bad E-Mail: Domain: ', server_string
        return False
    except NoAnswer:
        print 'NoAnswer for Domain: ', server_string
        return True
    else:
        return True
