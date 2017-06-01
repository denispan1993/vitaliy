# coding=utf-8
from django.db import models
from datetime import datetime, timedelta
import managers
from django.utils.translation import ugettext_lazy as _


def default_action_name():
    return u'Акция от %s' % datetime.now()


def default_datetime_end():
    return datetime.now() + timedelta(days=7, )


class Action(models.Model, ):
    name = models.CharField(verbose_name=u'Наименование акции',
                            max_length=256,
                            blank=False,
                            null=False,
                            default=default_action_name, )
    datetime_start = models.DateTimeField(verbose_name=u'Дата начала акции',
                                          default=datetime.now, )

    datetime_end = models.DateTimeField(verbose_name=u'Дата окончания акции',
                                        default=default_datetime_end, )
    auto_start = models.BooleanField(verbose_name=u'Авто старт', default=True, )
    auto_end = models.BooleanField(verbose_name=u'Авто стоп', default=True, )
    auto_del = models.BooleanField(verbose_name=u'Авто удаление акции', default=False, )
    deleted = models.BooleanField(verbose_name=u'Удаленная акция', default=False, )
    auto_del_action_from_product = models.BooleanField(verbose_name=u'Удаление акции из товара', default=False, )
    auto_del_action_price = models.BooleanField(verbose_name=u'Авто удаление акционной цены', default=True, )
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    objects = managers.Manager_Action()

    def __unicode__(self):
        return u'Акция: %s' % (self.name, )

    class Meta:
        db_table = 'Action'
        ordering = ['-created_at', ]
        verbose_name = u'Акция'
        verbose_name_plural = u'Акции'
