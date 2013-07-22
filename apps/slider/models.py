# coding=utf-8
from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.


class slide(models.Model):
    order = models.PositiveSmallIntegerField(verbose_name=_(u'Порядок сортировки'),
                                             # visibility=True,
                                             blank=True,
                                             null=True, )
    is_active = models.BooleanField(verbose_name=_(u'Актив. или Пасив.'), default=True, blank=False, null=False,
                                    help_text=u'Если мы хотим чтобы категория нигде не показывалась,'
                                              u' ставим данное поле в False.')
    slide = models.ImageField()
    title = models.CharField(verbose_name=u'Заголовок категории', max_length=255, null=False, blank=False, )
    name = models.CharField(verbose_name=u'Наименование категории', max_length=255, null=True, blank=True, )
    # visibility = models.BooleanField(verbose_name=u'Признак видимости категории', default=True, )

    # Вспомогательные поля
    # from django.contrib.contenttypes import generic
    # photo = generic.GenericRelation('Photo',
    #                                 content_type_field='content_type',
    #                                 object_id_field='object_id', )

    from compat.ImageWithThumbs import models
    photo =