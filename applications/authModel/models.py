# -*- coding: utf-8 -*-
import re
import warnings
from django.db import models
from django.conf import settings
from django.core import validators
from django.core.mail import send_mail
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, AbstractUser, UserManager, PermissionsMixin, )
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _

from applications.utils.captcha.utils import key_generator

__author__ = 'AlexStarov'


# Модифицируем поле email.
# _meta это экземпляр django.db.models.options.Options, который хранит данные о модели.
# Это немного хак, но я пока не нашел более простого способа переопределить поле из базовой модели.
#AbstractUser._meta.get_field('email')._unique = True
#AbstractUser._meta.get_field('username').max_length = 32
#AbstractUser._meta.get_field('username').help_text = _('Required. 32 characters or fewer. '
#                                                       'Letters, numbers and @/./+/-/_ characters', ),

#AbstractUser._meta.get_field('email').blank = True
#AbstractUser._meta.get_field('email')._null = True

#AbstractUser._meta.get_field('email').USERNAME_FIELD = 'username'
#AbstractUser._meta.get_field('email').REQUIRED_FIELDS = ['username', ]


class User(AbstractBaseUser, PermissionsMixin, ):
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
        (NONE, _(u'Не определено'), ),
        (MALE, _(u'Мужчина'), ),
        (FEMALE, _(u'Женщина'), ),
    )
    # Пол
    gender = models.PositiveSmallIntegerField(choices=gender_CHOICES,
                                              verbose_name=_(u'Пол'),
                                              default=NONE,
                                              blank=True,
                                              null=True, )
    # Номер телефона
    # phone = models.CharField(max_length=19,
    #                          verbose_name=_(u'Номер телефона'),
    #                          blank=True,
    #                          null=True, )
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
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    # def __unicode__(self):
    #     return u'Пользователь: %s' % (self.user, )

    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=32, unique=True,
                                help_text=_('Required. 32 characters or fewer. Letters, numbers and '
                                            '@/./+/-/_ characters', ),
                                validators=[
                                    validators.RegexValidator(re.compile('^[\w.@+-]+$'),
                                                              _('Enter a valid username.'),
                                                              'invalid', ),
                                ], )
    first_name = models.CharField(_('first name'), max_length=30, blank=True, )
    last_name = models.CharField(_('last name'), max_length=30, blank=True, )
    # email = models.EmailField(_('email address'), blank=True)

    """
        Заглушка
    """
    @property
    def email(self, ):
        emails = Email.email_parent_user.all()
        return None

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.', ), )
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.', ), )
    date_joined = models.DateTimeField(_('date joined', ), default=timezone.now, )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username, )

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name, )
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], )

    def get_profile(self):
        """
        Returns site-specific profile for this user. Raises
        SiteProfileNotAvailable if this site does not allow profiles.
        """
        # from django.contrib.auth.models import SiteProfileNotAvailable
        warnings.warn("The use of AUTH_PROFILE_MODULE to define user profiles has been deprecated.",
                      DeprecationWarning, stacklevel=2, )
        if not hasattr(self, '_profile_cache'):
            # if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
            #     raise SiteProfileNotAvailable(
            #         'You need to set AUTH_PROFILE_MODULE in your project '
            #         'settings', )
            try:
                app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            except ValueError:
                pass
                # raise SiteProfileNotAvailable(
                #     'app_label and model_name should be separated by a dot in '
                #     'the AUTH_PROFILE_MODULE setting')
            try:
                model = models.get_model(app_label, model_name)
                # if model is None:
                #     raise SiteProfileNotAvailable(
                #         'Unable to load the profile model, check '
                #         'AUTH_PROFILE_MODULE in your project settings')
                self._profile_cache = model._default_manager.using(
                                   self._state.db).get(user__id__exact=self.id)
                self._profile_cache.user = self
            except (ImportError, ImproperlyConfigured):
                pass
                # raise SiteProfileNotAvailable
        return self._profile_cache

    class Meta:
        db_table = u'UserModel'
        ordering = [u'-created_at', ]
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'

#User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


class Email(models.Model, ):
    user = models.ForeignKey(to=User,
                             verbose_name=_(u'Пользователь', ),
                             related_name='email_parent_user',
                             null=True,
                             blank=True, )
    hash = models.CharField(verbose_name=u'Hash',
                            unique=False,
                            max_length=16,
                            default=key_generator,
                            blank=False,
                            null=False, )
    # Тест e'mail
    test = models.BooleanField(
        verbose_name=_(u"Тест e'mail", ),
        default=False, )
    email = models.EmailField(_('email address'),
                              blank=False,
                              null=False, )
    description = models.TextField(_(u'Описание', ),
                                   blank=True,
                                   null=True,
                                   help_text=_(u'Поле с текстовым описанием'), )
    primary = models.BooleanField(verbose_name=_(u'Основной', ), default=False, )
    """
        E-Mail рассылки
    """
    # Рассылка Спам
    delivery_spam = models.BooleanField(verbose_name=_(u'Спам', ),
                                        default=True, )
    # Рассылка новых продуктов
    delivery_new_products = models.BooleanField(verbose_name=_(u'Новые продукты', ),
                                                default=True, )
    # Рассылка акций и новостей
    delivery_shares_news = models.BooleanField(verbose_name=_(u'Новости и Акции', ),
                                               default=True, )
    bad_email = models.BooleanField(verbose_name=_(u'Bad E-Mail', ),
                                    default=False, )
    error550 = models.BooleanField(verbose_name=_(u'Error 550', ),
                                   default=False, )
    error550_date = models.DateField(verbose_name=_(u'Error 550 Date', ),
                                     blank=True,
                                     null=True, )
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    @property
    def domain(self, ):
        return self.email.split('@')[1]

    @property
    def content_type(self, ):
        return ContentType.objects.get_for_model(model=self, for_concrete_model=True, )

    class Meta:
        db_table = u'EmailUserModel'
        ordering = [u'-created_at', ]
        verbose_name = u'Email пользователя'
        verbose_name_plural = u"Email'ы пользователей"


class Phone(models.Model, ):
    user = models.ForeignKey(to=User,
                             verbose_name=_(u'Пользователь', ),
                             related_name='phone_parent_user', )
    # Номер телефона
    phone = models.CharField(max_length=19,
                             verbose_name=_(u'Номер телефона'),
                             blank=False,
                             null=False, )
    int_code = models.PositiveSmallIntegerField(verbose_name=_(u'Код  телефона'),
                                                blank=True,
                                                null=True, )
    int_phone = models.PositiveIntegerField(verbose_name=_(u'Номер телефона'),
                                            blank=True,
                                            null=True, )
    primary = models.BooleanField(verbose_name=_(u'Основной', ), default=False, )
    """
        SMS рассылки
    """
    sms_notification = models.BooleanField(verbose_name=_(u'SMS Рассылка', ),
                                           default=True, )
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    class Meta:
        db_table = u'PhoneUserModel'
        ordering = [u'-created_at', ]
        verbose_name = u'Телефон пользователя'
        verbose_name_plural = u"Телефоны пользователей"
