# coding=UTF-8
from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile, UserenaLanguageBaseProfile


class Profile(UserenaLanguageBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile', )
#    favourite_snack = models.CharField(_('favourite snack'),
#                                       max_length=5)
    NONE = 0
    MALE = 1
    FEMALE = 2
#    from enum import Enum
#    gender_CHOICES = Enum(
#    gender_CHOICES = (
#        NONE, _('unknown'),
#        MALE, _('male'),
#        FEMALE, _('female'),
#    )
    gender_CHOICES = (
        (NONE, 'Неизвестно'),
        (MALE, 'Мужчина'),
        (FEMALE, 'Женсчина'),
    )
    gender = models.PositiveSmallIntegerField(choices=gender_CHOICES,
                                              verbose_name=_('gender'),
                                              default=NONE, )
    phone = models.CharField(max_length=19,
                             verbose_name=_('phone'), )
    # Отчество
    patronymic = models.CharField(max_length=32,
                                  verbose_name=_('patronymic'), )
    # Перевозчик
    carrier_CHOICES = (
        0, _(u'УкрПочта'),
        1, _(u'Новая почта'),
        2, _(u'Деливери'),
        3, _(u'ИнТайм'),
        4, _(u'Ночной Экспресс'),
    )
    carrier = models.PositiveSmallIntegerField(choices=carrier_CHOICES,
                                               verbose_name=_(u'Перевозчик'),
                                               default=1, )
    #День рождения
    birthday = models.DateField(verbose_name=_(u'День рождения'), )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Профайл:%s' % (self.user.username, )

    class Meta:
        db_table = u'Profile'
        ordering = [u'-created_at']
        verbose_name = u'Профайл'
        verbose_name_plural = u'Профайлы'
