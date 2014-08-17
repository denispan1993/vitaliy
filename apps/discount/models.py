# coding=utf-8
from django.db import models

#from django.contrib.auth.models import (
#    BaseUserManager, AbstractBaseUser, AbstractUser, )
# Create your models here.

# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
# from userena.models import UserenaBaseProfile, UserenaLanguageBaseProfile

from datetime import datetime, timedelta


class Action(models.Model, ):
    default_action_name = lambda: u'Акция от %s' % datetime.now()
    name = models.CharField(verbose_name=u'Наименование акции',
                            max_length=256,
                            blank=False,
                            null=False,
                            default=default_action_name(), )
    datetime_start = models.DateTimeField(verbose_name=u'Дата начала акции',
                                          default=datetime.now(), )

    default_datetime_end = lambda x: datetime.now() + timedelta(days=x, )
    datetime_end = models.DateTimeField(verbose_name=u'Дата окончания акции',
                                        default=default_datetime_end(7, ), )
    auto_start = models.BooleanField(verbose_name=u'Авто старт', default=True, )
    auto_end = models.BooleanField(verbose_name=u'Авто стоп', default=True, )
    auto_del = models.BooleanField(verbose_name=u'Авто удаление акции', default=False, )
    deleted = models.BooleanField(verbose_name=u'Удаленная акция', default=False, )
    auto_del_action_price = models.BooleanField(verbose_name=u'Авто удаление акционной цены', default=False, )
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    from apps.discount import managers
    objects = managers.Manager_Action()

    def __unicode__(self):
        return u'Акция: %s' % (self.name, )

    class Meta:
        db_table = u'Action'
        ordering = [u'-created_at', ]
        verbose_name = u'Акция'
        verbose_name_plural = u'Акции'

#User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
