# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'

from django.core.management.base import BaseCommand

from pytils.translit import slugify


class Command(BaseCommand, ):
    def handle(self, *args, **options):
        from apps.cart.models import Order
        from apps.authModel.models import User, Email, Phone
        from apps.account.models import Session_ID
        orders = Order.objects.filter(recompile=False, )
        i = 0
        from time import sleep
        for order in orders:
            # i += 1
            # if i > 300:
            #     break
            if 'user' in locals() or 'user' in globals():
                del user
            if 'email' in locals() or 'email' in globals():
                del email

            print order
            if order.user:
                continue
            # first_name = order.FIO.split()[1]
            # print first_name
            # order 1330 Михайленко Надежда Петровна                              НестеренкоО.В.                
            if '.' in order.FIO:
                FIO = order.FIO.split('.')
                FIO_temp = FIO
                if FIO[0][-1] == '.' and FIO[0][-3] == '.'\
                        or 'Діденко'.decode('utf-8') in FIO[0]\
                        or 'Коба'.decode('utf-8') in FIO[0]\
                        or 'Слободянюк'.decode('utf-8') in FIO[0]\
                        or 'Корягина'.decode('utf-8') in FIO[0]\
                        or 'Дуянова'.decode('utf-8') in FIO[0]\
                        or 'Тарасова'.decode('utf-8') in FIO[0]\
                        or 'Пашпадурова'.decode('utf-8') in FIO[0]\
                        or 'Розкошинская'.decode('utf-8') in FIO[0]:
                    FIO = FIO[0].split()
                    FIO[2] = FIO_temp[1]
                elif FIO[0][-1].isupper() and FIO[0][-2].isupper():
                    FIO[0] = FIO_temp[:-2]
                    FIO[1] = FIO_temp[-2]
                    FIO[2] = FIO_temp[-1]
            else:
                FIO = order.FIO.split()

            if len(FIO) == 3:
                last_name, first_name, patronymic = FIO
            elif len(FIO) == 2:
                last_name, first_name = FIO; patronymic = u'Отчество'
            elif len(FIO) == 1:
                last_name = FIO; first_name = u'Имя'; patronymic = u'Отчество'
            else:
                last_name = u'Фамилия'; first_name = u'Имя'; patronymic = u'Отчество'
            if last_name:
                print 'Order.Pk:', order.pk, ' last_name: ', last_name, ' type: ', type(last_name)
                if type(last_name, ) == list:
                    last_name
                    last_name[0]
                    last_name[0].encode('utf-8')
                    last_name[0].encode('UTF8')
                    unicode(last_name[0], )
                    last_name = unicode(last_name[0], ) # .encode('UTF8', ),
                    #temp = ''
                    #for x in last_name:
                    #    temp += x.encode('UTF8', )
                    #last_name = temp
                print 'Order.Pk:', order.pk, ' last_name: ', last_name, ' type: ', type(last_name)
                last_name = last_name.lstrip('.')
                if len(last_name, ) > 30:
                    print 'Order.Pk:', order.pk, ' last_name: ', last_name, ' type: ', type(last_name)
                    last_name = last_name[:30]
            if first_name:
                print 'Order.Pk:', order.pk, ' first_name: ', first_name, ' type: ', type(first_name)
                if type(first_name, ) == list:
                    first_name = unicode(first_name, ).encode('utf-8')
                print 'Order.Pk:', order.pk, ' first_name: ', first_name, ' type: ', type(first_name)
                first_name = first_name.lstrip('.')
                if len(first_name, ) > 30:
                    print 'Order.Pk:', order.pk, ' first_name: ', first_name, ' type: ', type(first_name)
                    first_name = first_name[:30]
            if patronymic:
                print 'Order.Pk:', order.pk, ' patronymic: ', patronymic, ' type: ', type(patronymic, ), 'len: ', len(patronymic, )
                if type(patronymic, ) == list:
                    patronymic = unicode(patronymic, ).encode('utf-8')
                print 'Order.Pk:', order.pk, ' patronymic: ', patronymic, ' type: ', type(patronymic, ), 'len: ', len(patronymic, )
                patronymic = patronymic.lstrip('.')
                if len(patronymic, ) > 32:
                    print 'Order.Pk:', order.pk, ' patronymic: ', patronymic, ' type: ', type(patronymic, ), 'len: ', len(patronymic, )
                    patronymic = patronymic[:32]
                print 'Order.Pk:', order.pk, ' patronymic: ', patronymic, ' type: ', type(patronymic, ), 'len: ', len(patronymic, )

            #last_name = last_name.stripe()
            #first_name = first_name.stripe()
            #patronymic = patronymic.stripe()
#            print first_name
#            print last_name
            # patronymic = order.FIO.split()[2]
#            print patronymic
            phone_temp = order.phone.split(' ', )
            print 'phone_temp: ', phone_temp
            try:
                if len(phone_temp[0], ) == 10 and len(phone_temp[3], ) == 10:
                    phone1 = phone_temp[0].strip().strip('-').strip('(').strip(')').lstrip('+380').lstrip('380').lstrip('80').lstrip('0')
                    print 'phone1: ', phone1
                    phone2 = phone_temp[3].strip().strip('-').strip('(').strip(')').lstrip('+380').lstrip('380').lstrip('80').lstrip('0')
                    print 'phone2: ', phone2
                elif len(phone_temp[0], ) == 11 and len(phone_temp[1], ) == 10:
                    phone1 = phone_temp[0].strip().strip('-').strip('(').strip(')').lstrip('+380').lstrip('380').lstrip('80').lstrip('0').rstrip(',')
                    print 'phone1: ', phone1
                    phone2 = phone_temp[1].strip().strip('-').strip('(').strip(')').lstrip('+380').lstrip('380').lstrip('80').lstrip('0')
                    print 'phone2: ', phone2
                elif len(phone_temp[0], ) == 11 and len(phone_temp[1], ) == 12:
                    phone1 = phone_temp[0].strip().strip('-').strip('(').strip(')').lstrip('+380').lstrip('380').lstrip('80').lstrip('0')
                    print 'phone1: ', phone1
                    phone2 = phone_temp[1].strip().strip('-').strip('(').strip(')').lstrip('+380').lstrip('380').lstrip('80').lstrip('0')
                    print 'phone2: ', phone2
                elif len(phone_temp[0], ) == 3 and len(phone_temp[1], ) == 3 and len(phone_temp[2], ) == 7 and len(phone_temp[3], ) == 12:
                    phone1 = phone_temp[0] + phone_temp[1] + phone_temp[2]
                    phone1 = phone1.strip().strip('-').strip('(').strip(')').lstrip('+380').lstrip('380').lstrip('80').lstrip('0').rstrip(',')
                    print 'phone1: ', phone1
                    phone2 = phone_temp[3].strip().strip('-').strip('(').strip(')').lstrip('+380').lstrip('380').lstrip('80').lstrip('0')
                    print 'phone2: ', phone2
                else:
                    for ph in phone_temp:
                        print 'phone_temp[n]: ', ph, 'len(ph, ):', len(ph, )
            except IndexError:
                print 'IndexError:'

            import re
            phone = re.sub("\D", "", order.phone, )
            phone = phone.strip().strip('-').strip('(').strip(')').lstrip('+380').lstrip('380').lstrip('80').lstrip('0')
            print 'Phone: ', phone
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
            print 'UserName: ', username
            sessionID = order.sessionid
            print sessionID

            try:
                sessionID = Session_ID.objects.get(sessionid=sessionID, )
            except Session_ID.DoesNotExist:
                sessionID_not_found = True
            else:
                if sessionID.user:
                    user = sessionID.user


            if 'user' not in locals() and 'user' not in globals():
                email = order.email.strip()
                print 'E-Mail1: ', email
            else:
                # email = user.email_parent_user.get()
                # print 'E-Mail 2.1: ', email
                email = user.email_parent_user.all()
                print 'E-Mail 2.2: ', email
                if not email:  # == []:
                    user.delete()
                else:
                    email = user.email_parent_user.all()[0]
                    print 'E-Mail 2.3: ', email.email
            import MySQLdb
            if type(email, ) != Email:
                try:
                    email = Email.objects.get(email=email, )
                except Email.DoesNotExist:
                    email_not_found = True
                except MySQLdb.Warning, e:
                    print e.args
                    print e.message
                    e_message = e.message.split(' ')[2]
                    print e_message
                    if e_message == 'DOUBLE':
                        try:
                            emails = Email.objects.filter(email=email, )
                        except:
                            pass
                        print emails
                        print len(emails, )
                        emails[0].delete()
                        try:
                            email = Email.objects.get(email=email, )
                        except:
                            pass
                    print e.__doc__
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
            except Phone.MultipleObjectsReturned:
                phones = Phone.objects.filter(phone=phone, )
                print len(phones, )
                if len(phones, ) > 1:
                    phones[0].delete()
                    phone = phones[1]
            else:
                if type(sessionID) != Session_ID and type(email) != Email:
                    user = phone.user
                else:
                    if ('user' in locals() or 'user' in globals()) and user == phone.user:
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
            if isinstance(email, unicode):  # type(email, ) == 'unicode':
                print 'email type: ', type(email, ), 'email: ', email
            else:
                print 'email type: ', type(email, ), 'email: ', email.email
            if email != None:
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

            sleep(1, )
            order.recompile = True
            order.save()

#            order.user = user
#            order.save()
