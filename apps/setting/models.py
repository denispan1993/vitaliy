# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Setting(models.Model):
    name = models.CharField(verbose_name=_(u'Наименование настройки', ),
                            max_length=128,
                            blank=False,
                            null=False,
                            default='', )
    variable_name = models.CharField(verbose_name=_(u'Имя переменной', ),
                                     max_length=128,
                                     unique=True,
                                     blank=False,
                                     null=False,
                                     default='', )
    variable = models.CharField(verbose_name=_(u'Переменная', ),
                                max_length=128,
                                blank=True,
                                null=True, )
    description = models.TextField(verbose_name=_(u'Описание настройки', ),
                                   blank=True,
                                   null=True, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, )
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, )

    from django.contrib.contenttypes import generic
    from apps.product.models import Photo
    photo = generic.GenericRelation(Photo,
                                    content_type_field='content_type',
                                    object_id_field='object_id', )

    def __unicode__(self, ):
        return u'%s - %s' % (self.name, self.variable_name, )

    class Meta:
        db_table = 'Setting'
        ordering = ['created_at', ]
        verbose_name = u'Настройка'
        verbose_name_plural = u'Настройки'
