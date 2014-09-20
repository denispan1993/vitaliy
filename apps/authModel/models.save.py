# coding=utf-8
from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, AbstractUser, UserManager, )
# Create your models here.

# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
# from userena.models import UserenaBaseProfile, UserenaLanguageBaseProfile


# Модифицируем поле email.
# _meta это экземпляр django.db.models.options.Options, который хранит данные о модели.
# Это немного хак, но я пока не нашел более простого способа переопределить поле из базовой модели.
#AbstractUser._meta.get_field('email')._unique = True
AbstractUser._meta.get_field('username').max_length = 32
AbstractUser._meta.get_field('username').help_text = _('Required. 32 characters or fewer. '
                                                       'Letters, numbers and @/./+/-/_ characters', ),

AbstractUser._meta.get_field('email').blank = True
AbstractUser._meta.get_field('email')._null = True

AbstractUser._meta.get_field('email').USERNAME_FIELD = 'username'
AbstractUser._meta.get_field('email').REQUIRED_FIELDS = ['username', ]


class User(AbstractUser, ):
    # import re
    # from django.core import validators

    # username = models.CharField(verbose_name=_('username'), max_length=32, unique=True,
    #                             validators=[
    #                                 validators.RegexValidator(re.compile('^[\w.@+-]+$'),
    #                                                           _('Enter a valid username.'),
    #                                                           'invalid')
    #                             ])
    # email = models.EmailField(verbose_name=_('email address'), blank=True, null=True, )
    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username', ]
    date_of_birth = models.DateField(verbose_name=u'День рождения', blank=True, null=True, )

    NONE = 0
    MALE = 1
    FEMALE = 2
    gender_CHOICES = (
        (NONE, _(u'Не определено')),
        (MALE, _(u'Мужчина')),
        (FEMALE, _(u'Женщина')),
    )
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
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['phone', ]
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
    email_delivery_new_products = models.BooleanField(verbose_name=_(u'Новые продукты', ),
                                                      default=True, )
    # Рассылка акций и новостей
    email_delivery_shares_news = models.BooleanField(verbose_name=_(u'Новости и Акции', ),
                                                     default=True, )
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    objects = UserManager()

    # def __unicode__(self):
    #     return u'Пользователь: %s' % (self.user, )

    class Meta:
        db_table = u'UserModel'
        ordering = [u'-created_at', ]
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'

#User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])

