# coding=utf-8
from django.db import models

# Create your models here.

from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile, UserenaLanguageBaseProfile


class Profile(UserenaLanguageBaseProfile):
    # Пользователь
#     Users = get_user_model()
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_(u'Пользователь'),
                                related_name='profile',
                                blank=False,
                                null=False, )
    # favourite_snack = models.CharField(_('favourite snack'),
    #                                    max_length=5, )
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
    # Населённый пункт
    settlement = models.CharField(max_length=32,
                                  verbose_name=_(u'Населённый пункт'),
                                  blank=True,
                                  null=True, )
    # Область
    area = models.CharField(max_length=32,
                            verbose_name=_(u'Область'),
                            blank=True,
                            null=True, )
    # Страна
    country = models.CharField(max_length=32,
                               verbose_name=_(u'Страна'),
                               default=u'Украина',
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
    """
        E-Mail рассылки
    """
    # Рассылка новых продуктов
#    email_delivery_new_products = models.BooleanField(verbose_name=_(u'Новые продукты', ),
#                                                      default=True, )
    # Рассылка акций и новостей
#    email_delivery_shares_news = models.BooleanField(verbose_name=_(u'Новости и Акции', ),
#                                                     default=True, )
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Профайл: %s' % (self.user, )

    class Meta:
        db_table = u'Profile'
        ordering = [u'-created_at', ]
        verbose_name = u'Профайл'
        verbose_name_plural = u'Профайлы'

#User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
