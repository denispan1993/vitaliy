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
            if 'user' in locals() or 'user' in globals():
                del user

            print order
            if order.user:
                continue
            # first_name = order.FIO.split()[1]
            # print first_name
            FIO = order.FIO.split()
            if len(FIO) == 3:
                last_name, first_name, patronymic = FIO
            elif len(FIO) == 2:
                last_name, first_name = FIO; patronymic = u'Отчество'
            elif len(FIO) == 1:
                last_name = FIO; first_name = u'Имя'; patronymic = u'Отчество'
            else:
                last_name = u'Фамилия'; first_name = u'Имя'; patronymic = u'Отчество'

            print 'Order.Pk:', order.pk, ' last_name: ', last_name, ' type: ', type(last_name)
            if type(last_name, ) == list:
                last_name = unicode(last_name, )
            print 'Order.Pk:', order.pk, ' last_name: ', last_name, ' type: ', type(last_name)
            if len(last_name, ) > 30:
                print 'Order.Pk:', order.pk, ' last_name: ', last_name, ' type: ', type(last_name)
                last_name = last_name[:30]
            print 'Order.Pk:', order.pk, ' first_name: ', first_name, ' type: ', type(first_name)
            if type(first_name, ) == list:
                first_name = unicode(first_name, )
            print 'Order.Pk:', order.pk, ' first_name: ', first_name, ' type: ', type(first_name)
            if len(first_name, ) > 30:
                print 'Order.Pk:', order.pk, ' first_name: ', first_name, ' type: ', type(first_name)
                first_name = first_name[:30]
            print 'Order.Pk:', order.pk, ' patronymic: ', patronymic, ' type: ', type(patronymic)
            if type(patronymic, ) == list:
                patronymic = unicode(patronymic, )
            print 'Order.Pk:', order.pk, ' patronymic: ', patronymic, ' type: ', type(patronymic)
            if len(patronymic, ) > 32:
                print 'Order.Pk:', order.pk, ' patronymic: ', patronymic, ' type: ', type(patronymic)
                patronymic = patronymic[:32]

            #last_name = last_name.stripe()
            #first_name = first_name.stripe()
            #patronymic = patronymic.stripe()
#            print first_name
#            print last_name
            # patronymic = order.FIO.split()[2]
#            print patronymic
            email = order.email.strip()
#            print email
            phone_temp = order.phone.split()
            print 'phone_temp: ', phone_temp
            try:
                if len(phone_temp[0], ) == 7 and len(phone_temp[1], ) == 7:
                    phone1 = phone_temp[0].strip().strip('-').strip('(').strip(')').lstrip('+380').lstrip('380').lstrip('80').lstrip('0')
                    print 'phone1: ', phone1
                    phone2 = phone_temp[1].strip().strip('-').strip('(').strip(')').lstrip('+380').lstrip('380').lstrip('80').lstrip('0')
                    print 'phone2: ', phone2
                else:
                    print 'phone1: ', phone1
                    print 'phone2: ', phone2
            except IndexError:
                print 'IndexError:'
            phone = order.phone.strip().strip('-').strip('(').strip(')').lstrip('+380').lstrip('380').lstrip('80').lstrip('0')
#            print phone
#            username = ''.join(['%s' % k.capitalize() for k in last_name, first_name, patronymic], )
#            print username
            username = ''.join(['%s' % slugify(k).capitalize() for k in last_name, first_name, patronymic], )
            print 'Order.Pk:', order.pk, ' username: ', username, ' type: ', type(username)
            if type(username, ) == list:
                username = str(username, )
            print 'Order.Pk:', order.pk, ' username: ', username, ' type: ', type(username)
            if len(username, ) > 32:
                print 'Order.Pk:', order.pk, ' username: ', username, ' type: ', type(username)
                username = username[:32]

            # username = slugify(username, )
            print username
            sessionID = order.sessionid
            print sessionID

            try:
                sessionID = Session_ID.objects.get(sessionid=sessionID, )
            except Session_ID.DoesNotExist:
                sessionID_not_found = True
            else:
                user = sessionID.user

            try:
                email = Email.objects.get(email=email, )
            except Email.DoesNotExist:
                email_not_found = True
            else:
                if type(sessionID) != Session_ID:
                    user = email.user
                else:
                    if email.user == sessionID.user:
                        print u'Ok', u' - ', u'SessionID.user == Email.user'
                    else:
                        print u'Хреново, Email и SessionID пренадлежат разным пользователям.'
                        print u'SessionID.user: ', sessionID.user
                        print u'Email.user: ', email.user
                        continue
            try:
                phone = Phone.objects.get(phone=phone, )
            except Phone.DoesNotExist:
                phone_not_found = True
            else:
                if type(sessionID) != Session_ID and type(email) != Email:
                    user = phone.user
                else:
                    if user == phone.user:
                        print u'Phone.user == User'
                    else:
                        print u'Номер телефона зарегистрирован за другим пользователем'
                        if type(sessionID) == Session_ID:
                            print u'SessionID.user: ', sessionID.user
                        if type(email) == Email:
                            print u'Email.user: ', email.user
                        print u'Phone.user: ', phone.user
                        continue

            if 'user' not in locals() and 'user' not in globals():
                try:
                    user = User.objects.get(username=username, )
                except User.DoesNotExist:
                    user = User.objects.create(username=username,
                                               first_name=first_name,
                                               last_name=last_name,
                                               patronymic=patronymic, )
            if type(sessionID) != Session_ID:
                sessionID = Session_ID.objects.create(user=user, sessionid=sessionID, )
            else:
                sessionID.user = user
                sessionID.save()

            if type(email) != Email:
                email = Email.objects.create(user=user, email=email, )
            else:
                email.user = user
                email.save()

            if type(phone) != Phone:
                if 'phone1' in locals() or 'phone1' in globals() and 'phone2' in locals() or 'phone2' in globals():
                    Phone.objects.create(user=user, phone=phone1, )
                    del phone1
                    Phone.objects.create(user=user, phone=phone2, )
                    del phone2
                else:
                    Phone.objects.create(user=user, phone=phone, )
            else:
                phone.user = user
                phone.save()

#            order.user = user
#            order.save()
