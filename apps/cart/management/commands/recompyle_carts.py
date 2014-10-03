# coding=utf-8
__author__ = 'user'

from django.core.management.base import BaseCommand

from pytils.translit import slugify


class Command(BaseCommand, ):
    def handle(self, *args, **options):
        from apps.cart.models import Order
        from apps.authModel.models import User, Email, Phone
        from apps.account.models import Session_ID
        orders = Order.objects.all()
        for order in orders:
            print order
            # first_name = order.FIO.split()[1]
            # print first_name
            last_name, first_name, patronymic = order.FIO.split()
            #last_name = last_name.stripe()
            #first_name = first_name.stripe()
            #patronymic = patronymic.stripe()
            print first_name
            print last_name
            # patronymic = order.FIO.split()[2]
            print patronymic
            email = order.email.strip()
            print email
            phone = order.phone.strip().strip('-').strip('(').strip(')').lstrip('+380').lstrip('380').lstrip('80').lstrip('0')
            print phone
            username = ''.join(['%s' % k.capitalize() for k in last_name, first_name, patronymic], )
            print username
            username = ''.join(['%s' % slugify(k).capitalize() for k in last_name, first_name, patronymic], )
            # username = slugify(username, )
            print username
            sessionID = order.sessionid
            print sessionID
            try:
                user = User.objects.filter(username=username, )
            except User.DoesNotExist:
                user = True
            if user == []:
                print user
                print username
                print u'Пользователь с таким username существует'
                continue
            else:
                try:
                    email = Email.objects.filter(email=email, )
                except Email.DoesNotExist:
                    email = True
                if email == []:
                    print email
                    print username
                    print u'Такой email существует у какогото пользователя'
                    continue
                else:
                    try:
                        phone = Phone.objects.filter(phone=phone, )
                    except Phone.DoesNotExist:
                        phone = True
                    if phone == []:
                        print phone
                        print username
                        print u'Такой номер телефона существует у какогото пользователя'
                        continue
                    else:
                        try:
                            sessionID = Session_ID.objects.filter(sessionid=sessionID, )
                        except Session_ID.DoesNotExist:
                            sessionID = True
                        if sessionID == []:
                            print sessionID
                            print u'Пользователь с таким SessionID уже существует'
                            continue
                        else:
                            user = User.objects.create(username=username,
                                                       first_name=first_name,
                                                       last_name=last_name,
                                                       patronymic=patronymic, )
                            email = Email.objects.create(user=user, email=email, )
                            phone = Phone.objects.create(user=user, phone=phone, )
                            sessionID = Session_ID.objects.create(user=user, sessionid=sessionID, )
                            order.user = user
                            order.save()
