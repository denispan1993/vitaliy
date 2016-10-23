# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from compat.ImageWithThumbs import models as ImageModels
import managers

__author__ = 'AlexStarov'


def set_path_photo(self, filename, ):
    return 'slide/%.2d/%s' % (
        # self.product.pub_datetime.year,
        self.order,
        filename, )


def default_slide_name():
    return u'Слайд от %s' % datetime.now()

OPENING_METHOD = ((1, '_blank'), (2, '_self'), )


class Slide(models.Model):

    name = models.CharField(verbose_name=_(u'Наименование слайда', ),
                            max_length=128,
                            blank=True,
                            null=True,
                            default=default_slide_name, )
    order = models.PositiveSmallIntegerField(verbose_name=_(u'Порядок сортировки', ),
                                             # visibility=True,
                                             db_index=True,
                                             unique=True,
                                             blank=True,
                                             null=True,
                                             help_text=u'Цифры от 1 до 99', )
    is_active = models.BooleanField(verbose_name=_(u'Актив. или Пасив', ),
                                    default=True,
                                    blank=False,
                                    null=False,
                                    help_text=u'Если мы хотим чтобы слайд не показывался,'
                                              u' ставим данное поле в False.')

    opening_method = models.PositiveSmallIntegerField(verbose_name=_(u'Метод открытия страницы слайда', ),
                                                      choices=OPENING_METHOD,
                                                      blank=False,
                                                      null=False,
                                                      default=1, )

    url = models.CharField(verbose_name=_(u'Url', ),
                           max_length=256,
                           blank=True,
                           null=True, )

    content_type = models.ForeignKey(ContentType,
                                     related_name='related_Slide',
                                     blank=True,
                                     null=True, )
    object_id = models.PositiveIntegerField(db_index=True,
                                            blank=True,
                                            null=True, )
    parent = GenericForeignKey('content_type', 'object_id', )

    title = models.CharField(verbose_name=u'title слайда',
                             max_length=255,
                             blank=True,
                             null=True,
                             default=u'title',
                             help_text=u'Верхняя строчка в описании слайда', )
    alt = models.CharField(verbose_name=u'alt слайда',
                           max_length=255,
                           null=True,
                           blank=True,
                           help_text=u'Строчка описания слайда для поисковых систем', )
    text = models.CharField(verbose_name=u'a слайда',
                            max_length=255,
                            null=True,
                            blank=True,
                            help_text=u'Нижняя строчка в описании слайда', )
    # visibility = models.BooleanField(verbose_name=u'Признак видимости категории', default=True, )

    # Вспомогательные поля
    # photo = generic.GenericRelation('Photo',
    #                                 content_type_field='content_type',
    #                                 object_id_field='object_id', )

    slide = ImageModels.ImageWithThumbsField(verbose_name=u'Слайд',
                                             upload_to=set_path_photo,
                                             sizes=((240, 96), (128, 48), ),
                                             blank=False,
                                             null=False,
                                             help_text=u'Слайд должен быть в разрешении 960x360', )
    #Дата создания и дата обновления новости. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, )
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, )

    manager = managers.ManagerSlide()

    def get_absolute_url(self, ):
        if self.content_type_id\
                and not self.content_type.app_label == 'slide'\
                and self.object_id\
                and not self.url:

            try:
                return self.content_type.get_object_for_this_type(id=self.object_id).get_absolute_url()
            except (ObjectDoesNotExist, AttributeError) as e:
                print('models.slide.get_absolute_url(): ', e, )

        if self.url and not self.content_type_id and not self.object_id:
            return self.url

        return '/'

    def __unicode__(self, ):
#        text = u'Активный' if self.is_active else text = u'Пасивный'
#        return u'Слайд: %s - %s %s' % (self.title, self.text, text, )
        if self.is_active:
            return u'Слайд: %s - %s Активный' % (self.title, self.text, )
        else:
            return u'Слайд: %s - %s Пасивный' % (self.title, self.text, )

    class Meta:
        db_table = 'Slide'
        ordering = ['order', ]
        verbose_name = u'Слайд'
        verbose_name_plural = u'Слайды'
