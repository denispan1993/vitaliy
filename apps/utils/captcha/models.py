# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


def set_path_photo(self, filename, ):
    return 'captcha/%.2d/%s' % (self.image_type, filename, )


class Captcha_Images(models.Model, ):
    Image_Type = (
        (1, _(u'Цветы', ), ),
#        (2, _(u'Грузовые машины', ), ),
        (3, _(u'Легковые машины', ), ),
#        (4, _(u'Мотоциклы машины', ), ),
#        (5, _(u'Велосипеды машины', ), ),
#        (6, _(u'Лица людей', ), ),
#        (7, _(u'Собаки', ), ),
#        (8, _(u'Кошки', ), ),
        (9, _(u'Дома', ), ),
    )
    image_type = models.PositiveSmallIntegerField(verbose_name=_(u'Тип картинки'),
                                                  choices=Image_Type,
                                                  default=1,
                                                  blank=False,
                                                  null=False, )

    image = models.ImageField(verbose_name=u'Картинка',
                              upload_to=set_path_photo,
                              blank=False,
                              null=False, )
    alt = models.CharField(verbose_name=u'Alt картинки',
                           max_length=64,
                           null=False,
                           blank=False, )

    #Дата создания и дата обновления записи. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Картинка: %s' % self.image

    class Meta:
        db_table = 'Captcha_Images'
#        ordering = ['serial_number', '-created_at', ]
        ordering = ['-created_at', ]
        verbose_name = u'Captcha картинка'
        verbose_name_plural = u'Captcha картинки'


class Captcha_Key(models.Model, ):
    from apps.utils.captcha.views import key_generator
    key = models.CharField(verbose_name=u'Капча код',
                           unique=True,
                           max_length=8,
                           default=key_generator,
                           blank=False,
                           null=False, )
    image = models.ForeignKey(Captcha_Images,
                              verbose_name=u'Ссылка на картинку', )
    image_type = models.PositiveSmallIntegerField(verbose_name=_(u'Тип картинки'),
                                                  default=0,
                                                  blank=False,
                                                  null=False, )

    from datetime import datetime
    next_use = models.DateTimeField(default=datetime.now, )

    #Дата создания и дата обновления записи. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    @property
    def update(self, ):
        # self.save()
        # from django.db.models import F
        # View.view_count = F('view_count') + 1
        from datetime import datetime, timedelta
        from django.utils import timezone
        """
            TypeError: can't compare offset-naive and offset-aware datetimes
            Несовместимость реального времени и времени со сдвигом тайм-зоны
            Нельзя сравнивать реальное время и время со сдвигом.
        """
        if self.created_at + timedelta(days=1, ) < timezone.now():
            """ Если дата ключа просрочена. Ключ убиваем. """
            self.delete()
            return None
        else:
            """ Закидываем на один час вперед время следующего использования данного ключа """
            timedelta = datetime.now() + timedelta(hours=1, )
            self.next_use = timedelta
            self.save()
            return self.key

    def save(self, *args, **kwargs):
        if self.image_type == 0:
            self.image_type = self.image.image_type
        super(Captcha_Key, self, ).save(*args, **kwargs)

#    @models.permalink
#    def get_absolute_url(self, ):
#        return ('show_category', (),
#                {'category_url': unicode(str(self.url)),
#                 'id': unicode(str(self.pk)), }, )
#        return u'/%s/к%.6d/' % (self.url, self.id, )

    def __unicode__(self):
        return u'Ключ: %s' % self.key

    class Meta:
        db_table = 'Captcha_Keys'
#        ordering = ['serial_number', '-created_at', ]
        ordering = ['-created_at', ]
        verbose_name = u'Captcha Ключ'
        verbose_name_plural = u'Captchas Ключи'
