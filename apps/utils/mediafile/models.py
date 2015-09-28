# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


def set_path(self, filename):
    return 'file/%.6d/%s' % (
        # self.product.pub_datetime.year,
        self.object_id,
        filename)


class MediaFile(models.Model):
    from django.contrib.contenttypes.models import ContentType
    content_type = models.ForeignKey(ContentType, related_name='related_MediaFile', )
    object_id = models.PositiveIntegerField(db_index=True, )
    from django.contrib.contenttypes import generic
    parent = generic.GenericForeignKey('content_type', 'object_id', )
    number = models.PositiveIntegerField(verbose_name=_(u'Номер файла в тексте', ),
                                         default=1,
                                         null=False,
                                         blank=False, )
    serial_number = models.PositiveIntegerField(verbose_name=_(u'Порядковы номер файла', ),
                                                default=1,
                                                null=False,
                                                blank=False, )
    main = models.NullBooleanField(verbose_name=u'Признак главного файла',
                                   null=False,
                                   blank=False,
                                   default=False, )

    height = models.PositiveIntegerField(verbose_name=_(u'Высота файла', ),
                                         default=1,
                                         null=True,
                                         blank=True, )
    width = models.PositiveIntegerField(verbose_name=_(u'Ширина файла', ),
                                        default=1,
                                        null=True,
                                        blank=True, )

#    from compat.ImageWithThumbs.fields import ImageWithThumbsField
    from compat.ImageWithThumbs import models as class_ImageWithThumb
    img = class_ImageWithThumb.ImageWithThumbsField(verbose_name=u'Изображение',
                                                    upload_to=set_path,
                                                    # sizes=((26, 26, ), (50, 50, ), (90, 95, ), ),
                                                    blank=True,
                                                    null=True, )
    title = models.CharField(verbose_name=u'Заголовок',
                             max_length=256,
                             null=True,
                             blank=True,
                             help_text=u'title \<a> записи.')
    name = models.CharField(verbose_name=u'Наименование',
                            max_length=256,
                            null=True,
                            blank=True, )
    sign = models.CharField(verbose_name=u'Подпись sign', max_length=128, blank=True, null=True,
                            help_text=u'Подпись которая буде написана под файлом.')
    description = models.TextField(verbose_name=u'Описание',
                                   null=True,
                                   blank=True, )
    #Дата создания и дата обновления новости. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    #Описание и ключевые слова для поисковиков
    meta_title = models.CharField(verbose_name=u'title',
                                  max_length=190,
                                  null=True,
                                  blank=True,
                                  help_text=u'Данный title читают поисковые системы для правильного расположения'
                                            u' файла в поиске.', )
    meta_alt = models.CharField(verbose_name=u'alt',
                                max_length=190,
                                null=True,
                                blank=True,
                                help_text=u'Данный alt читают поисковые системы для правильного расположения'
                                          u' файла в поиске.', )

#    def get_absolute_url(self, ):
#        return '/news/rubric/%s/' % self.url

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        self.img.field.sizes = ((self.height, self.width, ), )
        super(MediaFile, self).save(*args, **kwargs)  # Call the "real" save() method.

    def __unicode__(self):
        return u'Файл:%s' % (self.name, )

    class Meta:
        db_table = 'MediaFile'
        ordering = ['serial_number', '-created_at', ]
        verbose_name = "Медиа файл"
        verbose_name_plural = "Медиа файлы"
