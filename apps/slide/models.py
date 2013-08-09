# coding=utf-8
from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.


class Slide(models.Model):
    order = models.PositiveSmallIntegerField(verbose_name=_(u'Порядок сортировки'),
                                             # visibility=True,
                                             db_index=True,
                                             unique=True,
                                             blank=True,
                                             null=True,
                                             help_text=u'Цифры от 1 до 99', )
    is_active = models.BooleanField(verbose_name=_(u'Актив. или Пасив.'), default=True, blank=False, null=False,
                                    help_text=u'Если мы хотим чтобы слайд не показывался,'
                                              u' ставим данное поле в False.')
    from django.contrib.contenttypes.models import ContentType
    # from apps.product.models import Product
    content_type = models.ForeignKey(ContentType,
                                     related_name='related_Slide',
                                     blank=True,
                                     null=True, )
    object_id = models.PositiveIntegerField(db_index=True,
                                            blank=True,
                                            null=True, )
    from django.contrib.contenttypes import generic
    parent = generic.GenericForeignKey('content_type', 'object_id', )

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
    # from django.contrib.contenttypes import generic
    # photo = generic.GenericRelation('Photo',
    #                                 content_type_field='content_type',
    #                                 object_id_field='object_id', )

    def set_path_photo(self, filename, ):
        return 'slide/%.2d/%s' % (
            # self.product.pub_datetime.year,
            self.order,
            filename, )

    from compat.ImageWithThumbs import models as ImageModels
    slide = ImageModels.ImageWithThumbsField(verbose_name=u'Слайд',
                                             upload_to=set_path_photo,
                                             sizes=((240, 96), ),
                                             blank=False,
                                             null=False,
                                             help_text=u'Слайд должен быть в разрешении 960x360', )
    #Дата создания и дата обновления новости. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, )
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, )

    from apps.slide import managers
    manager = managers.Manager_Slide()

    @property
    def url(self, ):
        return self.parent.get_absolute_url()

    def __unicode__(self, ):
        if self.is_active:
            return u'Слайд: %s - %s Активный' % (self.title, self.text, )
        else:
            return u'Слайд: %s - %s Пасивный' % (self.title, self.text, )

    class Meta:
        db_table = 'Slide'
        ordering = ['order', ]
        verbose_name = u'Слайд'
        verbose_name_plural = u'Слайды'
