# -*- coding: utf-8 -*-
# /applications/comment/models.py
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from mptt.models import MPTTModel, TreeForeignKey

from proj import settings
from applications.comment import managers

COMMENT_TYPES = (
    (0, 'comment'),  # Комментарий
    (1, 'opinion'),  # Отзыв
)


class Comment(MPTTModel, ):
    type = models.PositiveSmallIntegerField(choices=COMMENT_TYPES, blank=True, null=True, )

    comment_parent = TreeForeignKey(
        to='Comment',
        verbose_name=_(u'Комментарий на который отвечает этот комментарий', ),
        blank=True,
        null=True,
        related_name=u'children', )
    """ Ссылка на главную запись """
    content_type = models.ForeignKey(
        to=ContentType,
        related_name='related_Product',
        blank=True,
        null=True, )
    object_id = models.PositiveIntegerField(db_index=True,
                                            blank=True,
                                            null=True, )
    record_parent = GenericForeignKey('content_type', 'object_id', )

    serial_number = models.PositiveSmallIntegerField(verbose_name=_(u'Порядок сортировки', ),
                                                     # visibility=True,
                                                     default=1,
                                                     blank=True,
                                                     null=True, )
    is_active = models.BooleanField(verbose_name=_(u'Актив. или Пасив.'),
                                    blank=False,
                                    null=False,
                                    default=True,
                                    help_text=u'Если мы хотим чтобы комментарий не показывался,'
                                              u' ставим данное поле в False.')
    shown_colored = models.BooleanField(verbose_name=_(u'Выделить цветом'),
                                        default=False,
                                        blank=False,
                                        null=False,
                                        help_text=u'Если мы хотим чтобы комментарий был выделен цветом Фуксия,'
                                                  u' ставим данное поле в True.')
    shown_bold = models.BooleanField(verbose_name=_(u'Выделить жирным'),
                                     default=False,
                                     blank=False,
                                     null=False,
                                     help_text=u'Если мы хотим чтобы комментарий был выделен жирным шрифтом,'
                                               u' ставим данное поле в True.')
    shown_italic = models.BooleanField(verbose_name=_(u'Выделить курсивом'),
                                       default=False,
                                       blank=False,
                                       null=False,
                                       help_text=_(u'Если мы хотим чтобы комментарий был выделен наклонным шрифтом,'
                                                   u' ставим данное поле в True.', ), )
    font_px = models.PositiveSmallIntegerField(verbose_name=_(u'Размер шрифта'),
                                               default=14,
                                               blank=False,
                                               null=False,
                                               help_text=_(u'Размер шрифта комментария в пикселях,', ), )
    """ Кто создал комментарий """
    name = models.CharField(verbose_name=_(u'Имя комментатора'),
                            default=None,
                            max_length=64,
                            null=False,
                            blank=False,
                            help_text=_(u'Как человек представился, имя которое будет выводится на сайте.'), )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             verbose_name=u'Пользователь',
                             null=True,
                             blank=True, )
    sessionid = models.CharField(verbose_name=u'SessionID',
                                 max_length=32,
                                 null=True,
                                 blank=True, )
    """ Заголовок комментария """
    title = models.TextField(verbose_name=_(u'Заголовок комментария', ), blank=True, null=True, )
    """ Собственно сам комментарий """
    comment = models.TextField(verbose_name=_(u'Комментарий', ), null=False, blank=False, )
    rating = models.SmallIntegerField(verbose_name=_(u'Рейтинг', ), null=True, blank=True, )
    pass_moderation = models.BooleanField(verbose_name=_(u'Флаг модерации', ),
                                          default=False,
                                          null=False,
                                          blank=False,
                                          help_text=_(u'Если стоит галочка, то комментарий прошел модерацию.', ), )
    require_a_response = models.BooleanField(verbose_name=_(u'Запрос ответа', ),
                                             default=False,
                                             null=False,
                                             blank=False,
                                             help_text=_(u'Пользователь запросил ответ на свой комментарий.', ), )
    email = models.CharField(verbose_name=_(u'E-Mail пользователя', ),
                             default=None,
                             max_length=64,
                             null=True,
                             blank=True,
                             help_text=_(u'E-Mail пользователя на который нужно отослать ссылку'
                                         u' на ответ на комментарий.', ), )
    phone = models.CharField(verbose_name=_(u'Телефон пользователя', ),
                             default=None,
                             max_length=32,
                             null=True,
                             blank=True, )
    #Дата создания и дата обновления комментария. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    objects = managers.Manager()

    def get_absolute_url(self, ):
        if self.type == 1:
            if self.title:
                return reverse(viewname='opinion_en:opinion_long',
                               kwargs={'opinion_url': slugify(value=self.title), 'pk': self.pk, }, )

            else:
                title = self.title
                url = slugify(value=self.title)
                pk = self.pk
                return reverse(viewname='opinion_en:opinion_short',
                               kwargs={'pk': self.pk, }, )

        if self.content_type:
            object = self.content_type.get_object_for_this_type(pk=self.object_id, )
            url = object.get_absolute_url()
            return u'%sкомментарий/%.6d/' % (url, self.pk, )
        else:
            return u'%d-/Имя/%s' % (self.pk, self.name, )

    def __str__(self):
        # """
        # Проверка DocTest
        # >>> category = Category.objects.create(title=u'Proverka123  -ф123')
        # >>> category.item_description = u'Тоже проверка'
        # >>> category.save()
        # >>> if type(category.__str__()) is unicode:
        # ...     print category.__str__() #.encode('utf-8')
        # ... else:
        # ...     print type(category.__str__())
        # ...
        # Категория: Proverka123  -ф123
        # >>> print category.title
        # Proverka123  -ф123
        # """
        return u'Комментарий: %s' % self.name

    class MPTTMeta:
        parent_attr = 'comment_parent'
        level_attr = 'mptt_level'
        order_insertion_by = ['name', ]

    class Meta:
        db_table = 'Comment'
        ordering = ['-created_at', ]
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'
