# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from smtplib import SMTPSenderRefused, SMTPDataError

from apps.delivery.models import Delivery, EmailMiddleDelivery, EmailForDelivery
from apps.delivery.utils import Mail_Account, get_email, create_msg, connect, send_msg
from apps.authModel.models import Email


__author__ = 'AlexStarov'


class Command(BaseCommand, ):
    from optparse import make_option
    option_list = BaseCommand.option_list + (
        make_option('--id', '--pk', '--delivery_id', '--delivery_pk',
                    action='store', type='int', dest='delivery_pk',
                    help=''),
        make_option('--t', '--delivery_test', '--test',
                    action='store_true', dest='delivery_test',
                    help=''),
        make_option('--g', '--delivery_general', '--general',
                    action='store_true', dest='delivery_test',
                    help=''),
    )
    #self.verbosity = int(options.get('verbosity'))
    #def add_arguments(self, parser):
    #    parser.add_argument('delivery_id', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            deliveryes = Delivery.objects.filter(delivery_test=True, send_test=False, )
        except Delivery.DoesNotExist:
            deliveryes = None
        else:
            for delivery in deliveryes:
                # print 'delivery', delivery
                try:
                    EmailMiddleDelivery.objects.\
                        get(delivery=delivery,
                            delivery_test_send=True,
                            delivery_send=False,
                            updated_at__lte=delivery.updated_at, )
                    #print aaa, delivery.updated_at
                except:
                    """ Создаем ссылочку на отсылку рассылки """
                    email_middle_delivery = EmailMiddleDelivery()
                    email_middle_delivery.delivery = delivery
                    email_middle_delivery.delivery_test_send = True
                    email_middle_delivery.delivery_send = False
                    email_middle_delivery.save()
                    """ Закрываем отсылку теста в самой рассылке """
                    delivery.send_test = True
                    delivery.save()

                    real_email = get_email(delivery=delivery, email_class=Email, pk=6, ) # pk=2836, )  # subscribe@keksik.com.ua
                    email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                                                            now_email=real_email,
                                                            email=real_email, )
                    """ Отсылаем тестовое письмо """
                    mail_account = Mail_Account(pk=1, )
                    msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, test=True, )

                    try:
                        connection = connect(mail_account=mail_account, fail_silently=False, )
                    except SMTPSenderRefused as e:
                        print 'SMTPSenderRefused: ', e
                        # email.delete()
                        # print 'SMTPSenderRefused'
                        # sleep(30, )
                        # time += 30
                    except SMTPDataError as e:
                        print 'SMTPDataError: ', e
                        # email.delete()
                        # print 'SMTPDataError'
                        # sleep(30, )
                        # time += 30
                    except Exception as e:
                        print 'Exception: ', e
                        if "(554, '5.7.1 Message rejected under suspicion of SPAM; http://help.yandex.ru/mail/spam/sending-limits.xml" in e:
                            print 'SPAM Bloked E-Mail: ', mail_account, ' NOW !!!!!!!!!!!!!!!!!!!!!!!'
                            from datetime import datetime
                            mail_account.is_auto_active = False
                            mail_account.auto_active_datetime = datetime.now()
                            mail_account.save()
                        connection = connect(mail_account=mail_account, fail_silently=True, )
                        msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, exception=e, test=True, )
                        send_msg(connection=connection, mail_account=mail_account, email=email, msg=msg, )
                    else:
                        send_msg(connection=connection, mail_account=mail_account, email=email, msg=msg, )

                    real_email = get_email(delivery=delivery, email_class=Email, pk=7, ) # pk=3263, )  # check-auth2@verifier.port25.com
                    from apps.delivery.models import EmailForDelivery

                    email = EmailForDelivery.objects.create(delivery=email_middle_delivery,
                                                            now_email=real_email,
                                                            email=real_email, )
                    msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, test=True, )
                    from smtplib import SMTPSenderRefused, SMTPDataError
                    try:
                        connection = connect(mail_account=mail_account, fail_silently=False, )
                    except SMTPSenderRefused as e:
                        print 'SMTPSenderRefused: ', e
                    except SMTPDataError as e:
                        print 'SMTPDataError: ', e
                    except Exception as e:
                        print 'Exception: ', e
                        if "(554, '5.7.1 Message rejected under suspicion of SPAM; http://help.yandex.ru/mail/spam/sending-limits.xml" in e:
                            print 'SPAM Bloked E-Mail: ', mail_account, ' NOW !!!!!!!!!!!!!!!!!!!!!!!'
                            from datetime import datetime
                            mail_account.is_auto_active = False
                            mail_account.auto_active_datetime = datetime.now()
                            mail_account.save()
                        connection = connect(mail_account=mail_account, fail_silently=True, )
                        msg = create_msg(delivery=delivery, mail_account=mail_account, email=email, exception=e, test=True, )
                        send_msg(connection=connection, mail_account=mail_account, email=email, msg=msg, )
                    else:
                        send_msg(connection=connection, mail_account=mail_account, email=email, msg=msg, )
