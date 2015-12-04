# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class LeadingCourse(models.Model):
    surname = models.CharField(verbose_name=_(u'Фамилия', ),
                               max_length=128,
                               blank=False,
                               null=False,
                               default=u'Фамилия', )
    name = models.CharField(verbose_name=_(u'Имя', ),
                               max_length=128,
                               blank=False,
                               null=False,
                               default=u'Имя', )
    patronymic = models.CharField(verbose_name=_(u'Отчество', ),
                               max_length=128,
                               blank=True,
                               null=True, )
    from compat.FormSlug import models as class_FormSlugField
    url = class_FormSlugField.ModelSlugField(verbose_name=u'URL адрес Ведущего',
                                             max_length=255,
                                             null=True,
                                             blank=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    @models.permalink
    def get_absolute_url(self, ):
        return ('calendar:leading_course_ru', (),
                {'leading_course_url': unicode(str(self.url)), }, )
#                 'id': unicode(str(self.pk)), }, )
#        return u'/%s/к%.6d/' % (self.url, self.id, )

    def __unicode__(self):
        return u'Ведущий(ая) курсы:%s %s%s' % (self.surname, self.name, ' %s' % self.patronymic if self.patronymic else '')

    class Meta:
        db_table = u'CalendarLeadingCourse'
        ordering = [u'-created_at']
        verbose_name = u'Ведущий(ая) курса'
        verbose_name_plural = u'Ведущие(ии) курсов'


class LocationDateTime(models.Model, ):
    from apps.product.models import City
    city = models.ForeignKey(to=City,
                             verbose_name=_(u'Город', ),
                             blank=False,
                             null=False,
                             default=1, )
    from datetime import datetime, date
    date_start = models.DateField(verbose_name=_(u'Дата начала мероприятия', ),
                                  blank=False,
                                  null=False,
                                  default=date.today, )
    date_end = models.DateField(verbose_name=_(u'Дата окончания мероприятия', ),
                                blank=False,
                                null=False,
                                default=date.today, )
    from django.utils.timezone import now
    time_start = models.TimeField(verbose_name=_(u'Время начала мероприятия', ),
                                  blank=False,
                                  null=False,
                                  default=now, )
    time_end = models.TimeField(verbose_name=_(u'Время окончания мероприятия', ),
                                blank=False,
                                null=False,
                                default=now, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Место проведения:%s %s - %s' % (self.city,
                                                 self.date_start.strftime("%d-%m-%Y"),
                                                 self.date_end.strftime("%d-%m-%Y"), )

    class Meta:
        db_table = u'CalendarLocationDateTime'
        ordering = [u'-created_at']
        verbose_name = u'Место Дата Время'
        verbose_name_plural = u'Места Даты Время'


class Subject(models.Model):
    subject = models.CharField(verbose_name=_(u'Тема мероприятия', ),
                               max_length=256,
                               blank=False,
                               null=False,
                               default=u'Тема мероприятия', )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Тема мероприятия: %s' % self.subject

    class Meta:
        db_table = u'CalendarSubject'
        ordering = [u'-created_at']
        verbose_name = u'Тема'
        verbose_name_plural = u'Темы'

class Event(models.Model):
    """
    Событие
    """
    # from django.contrib.auth.models import User
    from proj.settings import AUTH_USER_MODEL
    user = models.ForeignKey(to=AUTH_USER_MODEL,
                             verbose_name=u'Пользователь',
                             null=True,
                             blank=True, )
    sessionid = models.CharField(verbose_name=u'SessionID',
                                 max_length=32,
                                 null=True,
                                 blank=True, )
    leading_course = models.ForeignKey(to=LeadingCourse,
                                       verbose_name=_(u'Ведущий(ая) курсы', ),
                                       blank=False,
                                       null=False,
                                       default=1, )
    subject = models.ForeignKey(to=Subject,
                                verbose_name=_(u'Тема курса', ),
                                blank=False,
                                null=False,
                                default=1, )
    location_date_time = models.ManyToManyField(to=LocationDateTime,
                                                verbose_name=_(u'Место дата и время проведения', ),
                                                blank=False,
                                                null=False, )
                                                # default=1, )
    title = models.CharField(verbose_name=_(u'Наименование', ),
                             max_length=256,
                             blank=False,
                             null=False,
                             default=_(u'Событие', ), )
    description = models.TextField(verbose_name=_(u'Описание события', ),
                                   blank=True,
                                   null=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    from apps.calendar.managers import Manager
    objects = Manager()

    # Вспомогательные поля
    #from django.contrib.contenttypes import generic
    #cart = generic.GenericRelation('Product',
    #                               content_type_field='content_type',
    #                               object_id_field='object_id', )

    #@property
    #def products(self, ):
    #    return self.cart.all()

    #""" Возвращает целое число суммы корзины """
    #def sum_money_of_all_products_integral(self, request, ):
    #    return int(self.sum_money_of_all_products(request=request, ), )

    def __unicode__(self):
        return u'Событие:%s' % (self.title, )  # self.session.session_key, )

    class Meta:
        db_table = u'Calendar'
        ordering = [u'-created_at']
        verbose_name = u'Собитие'
        verbose_name_plural = u'События'
