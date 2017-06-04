# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from compat.FormSlug import models as class_FormSlugField
from applications.product.models import City
from datetime import datetime, date
from django.utils.timezone import now

__author__ = 'AlexStarov'


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
    url = class_FormSlugField.ModelSlugField(verbose_name=u'URL адрес Ведущего',
                                             max_length=255,
                                             null=True,
                                             blank=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    @models.permalink
    def get_absolute_url(self, ):
        if self.url:
            return ('calendar:leading_course_ru', (),
                    {'leading_course_url': self.url, }, )
        else:
            return ('calendar:leading_course_ru', (),
                    {'leading_course_url': 'None', }, )

    def __unicode__(self):
        return u'Ведущий(ая) курсы:%s %s%s' % (self.surname, self.name, ' %s' % self.patronymic if self.patronymic else '')

    class Meta:
        db_table = u'CalendarLeadingCourse'
        ordering = [u'-created_at']
        verbose_name = u'Ведущий(ая) курса'
        verbose_name_plural = u'Ведущие(ии) курсов'


class CoordinatorCourse(models.Model):
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
    url = class_FormSlugField.ModelSlugField(verbose_name=u'URL адрес Ведущего',
                                             max_length=255,
                                             null=True,
                                             blank=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Координатор:%s %s%s' % (self.surname, self.name, ' %s' % self.patronymic if self.patronymic else '')

    class Meta:
        db_table = u'CalendarCoordinatorCourse'
        ordering = [u'-created_at']
        verbose_name = u'Координатор курса'
        verbose_name_plural = u'Координаторы курсов'


class LocationDate(models.Model, ):
    city = models.ForeignKey(to=City,
                             verbose_name=_(u'Город', ),
                             blank=False,
                             null=False,
                             default=1, )
    date_start = models.DateField(verbose_name=_(u'Дата начала мероприятия', ),
                                  blank=False,
                                  null=False,
                                  default=date.today, )
    coordinator = models.ForeignKey(to=CoordinatorCourse,
                                    verbose_name=_(u'Координатор курса', ),
                                    blank=False,
                                    null=False,
                                    default=1, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Место проведения:%s %s' % (self.city,
                                            self.date_start.strftime("%d-%m-%Y"), )

    class Meta:
        db_table = u'CalendarLocationDate'
        ordering = [u'-created_at']
        verbose_name = u'Место Дата Время'
        verbose_name_plural = u'Места Даты Время'


class Section(models.Model):
    section = models.CharField(verbose_name=_(u'Раздел мероприятия', ),
                               max_length=256,
                               blank=False,
                               null=False,
                               default='', )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Раздел мероприятия: %s' % self.section

    class Meta:
        db_table = 'CalendarSection'
        ordering = ['-created_at']
        verbose_name = u'Раздел'
        verbose_name_plural = u'Разделы'


class Event(models.Model):
    """
    Событие
    """
    # from django.contrib.auth.models import User
    from proj.settings import AUTH_USER_MODEL
    user = models.ForeignKey(to=AUTH_USER_MODEL,
                             verbose_name=_(u'Пользователь'),
                             null=True,
                             blank=True, )
    sessionid = models.CharField(verbose_name='SessionID',
                                 max_length=32,
                                 null=True,
                                 blank=True, )
    section = models.ForeignKey(to=Section,
                                verbose_name=_(u'Раздел курса', ),
                                blank=False,
                                null=False,
                                default=1, )
    topic = models.CharField(verbose_name=_(u'Тема курса', ),
                             max_length=256,
                             blank=False,
                             null=False,
                             default='', )
    leading_course = models.ForeignKey(to=LeadingCourse,
                                       verbose_name=_(u'Ведущий(ая) курсы', ),
                                       blank=False,
                                       null=False,
                                       default=1, )
    location_date = models.ManyToManyField(to=LocationDate,
                                           verbose_name=_(u'Город и время проведения'),
                                           blank=False, )
    duration_days = models.PositiveSmallIntegerField(verbose_name=_(u'Продолжительность в днях', ),
                                                     blank=True,
                                                     null=True, )
    duration_hours = models.PositiveSmallIntegerField(verbose_name=_(u'Продолжительность в часах', ),
                                                      blank=True,
                                                      null=True, )
    description = models.TextField(verbose_name=_(u'Описание события', ),
                                   blank=True,
                                   null=True, )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    from applications.mycalendar import managers
    objects = managers.Manager()

    @property
    def location_date_gte_today(self):
        try:
            """ gte больше или равно """
            return self.location_date.filter(date_start__gte=datetime.today(),).distinct()
            #events = Event.objects\
            #    .filter(location_date_time__date_start__gte=datetime.today(), )\
            #    .distinct()
        except Event.DoesNotExist:
            return False

    def __unicode__(self):
        return u'Событие:%s' % (self.title, )  # self.session.session_key, )

    class Meta:
        db_table = 'Calendar'
        ordering = ['-created_at']
        verbose_name = u'Событие'
        verbose_name_plural = u'События'
