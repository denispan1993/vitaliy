# coding=utf-8

from models import Profile

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User, )
def AutoCreate_Profile(sender, instance, created, **kwargs):
    print u"Вход в создание профайла"
    if created:
        print u"Создание профайла"
        profile, created = Profile.objects.get_or_create(user=instance, )
        print(profile)
        print(created)






# coding=utf-8

from models import Profile

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
# from django.dispatch import dispatcher

# @receiver(post_save, sender=User, dispatch_uid='AutoCreate_Profile', )
def AutoCreate_Profile(sender, instance, created, signal, *args, **kwargs):
    print 'Enter to create Profile'
    if created:
        print 'Create Profile'
        # profile, created =
        try:
            print 'All OK!!!'
            print sender
            print instance
            Profile.objects.create(user=instance, )
            print 'All Good!!!!'
        except Profile.DoesNotExist:
            print 'Help!!!!!!'
        except TypeError:
            print 'My TypeError!!!!!!!#'
        else:
            print'All Very GOOOOOOOOODDDDDDDDDDD!!!!!!!!!!!!!'
        finally:
            print 'Finita Lya Comedy ;-('
        #Profile.objects.get_or_create(user=instance, )
        # print(profile)
        # print(created)

#dispatcher.connect(AutoCreate_Profile, signal=post_save, sender=User, )
post_save.connect(receiver=AutoCreate_Profile, sender=User, dispatch_uid='AutoCreate_Profile', )




NONE = 0
MALE = 1
FEMALE = 2
#    from enum import Enum
#    gender_CHOICES = Enum(
gender_CHOICES = (
    (NONE, _(u'Не определено')),
    (MALE, _(u'Мужчина')),
    (FEMALE, _(u'Женщина')),
)
#    gender_CHOICES = (
#        (NONE, 'Неизвестно'),
#        (MALE, 'Мужчина'),
#        (FEMALE, 'Женсчина'),
#    )
# Пол
gender = models.PositiveSmallIntegerField(choices=gender_CHOICES,
                                          verbose_name=_(u'Пол'),
                                          default=NONE,
                                          blank=True,
                                          null=True, )
# Номер телефона
phone = models.CharField(max_length=19,
                         verbose_name=_(u'Номер телефона'),
                         blank=True,
                         null=True, )
# Отчество
patronymic = models.CharField(max_length=32,
                              verbose_name=_(u'Отчество'),
                              blank=True,
                              null=True, )
# Перевозчик
carrier_CHOICES = (
    (0, _(u'Самовывоз')),
    (1, _(u'Новая почта')),
    (2, _(u'УкрПочта')),
    (3, _(u'Деливери')),
    (4, _(u'ИнТайм')),
    (5, _(u'Ночной Экспресс')),
)
carrier = models.PositiveSmallIntegerField(choices=carrier_CHOICES,
                                           verbose_name=_(u'Перевозчик'),
                                           default=1,
                                           blank=True,
                                           null=True, )
# День рождения
birthday = models.DateField(verbose_name=_(u'День рождения'),
                            blank=True,
                            null=True, )
