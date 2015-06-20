# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class FeedBack(models.Model, ):
    is_active = models.BooleanField(verbose_name=_(u'Актив. или Пасив.'), default=True, blank=False, null=False,
                                    help_text=u'Если мы хотим чтобы комментарий не показывался,'
                                              u' ставим данное поле в False.')
    """ Кто создал """
    from proj.settings import AUTH_USER_MODEL
    user = models.ForeignKey(to=AUTH_USER_MODEL,
                             verbose_name=u'Пользователь',
                             null=True,
                             blank=True, )
    sessionid = models.CharField(verbose_name=u'SessionID',
                                 max_length=32,
                                 null=True,
                                 blank=True, )
    name = models.CharField(verbose_name=_(u'Имя'),
                            default=None,
                            max_length=64,
                            null=False,
                            blank=False,
                            help_text=_(u'Как человек представился, имя которое будет выводится на сайте.'), )
    """ Собственно сам комментарий """
    comment = models.TextField(verbose_name=_(u'Комментарий', ), null=False, blank=False, )
    pass_moderation = models.BooleanField(verbose_name=_(u'Флаг модерации', ),
                                          default=False,
                                          null=False,
                                          blank=False,
                                          help_text=_(u'Если стоит галочка, то комментарий прошел модерацию.', ), )
    email_for_response = models.EmailField(verbose_name=_(u'E-Mail пользователя', ),
                                           default=None,
                                           max_length=64,
                                           null=True,
                                           blank=True,
                                           help_text=_(u'E-Mail пользователя на который нужно отослать ссылку'
                                                       u' на ответ на комментарий.', ), )
    #Дата создания и дата обновления комментария. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    # Вспомогательные поля
    from django.contrib.contenttypes import generic
    # from apps.product.models import Product
    # product = generic.GenericRelation(Product,
    #                                   content_type_field='content_type',
    #                                   object_id_field='object_id', )

    # objects = models.Manager()
    from apps.comment import managers
    objects = managers.Manager()

#    @models.permalink
    def get_absolute_url(self, ):
#        return ('show_product', (),
#                {'product_url': self.url,
#                 'id': self.pk, }, )
        # model = self.content_type.model_class()
        # object = model.objects.get(pk=self.object_id, )
        # url = object.get_absolute_url()
        object = self.content_type.get_object_for_this_type(pk=self.object_id, )
        url = object.get_absolute_url()
        return u'%sкомментарий/%.6d/' % (url, self.pk, )

    def __unicode__(self):
        # """
        # Проверка DocTest
        # >>> category = Category.objects.create(title=u'Proverka123  -ф123')
        # >>> category.item_description = u'Тоже проверка'
        # >>> category.save()
        # >>> if type(category.__unicode__()) is unicode:
        # ...     print category.__unicode__() #.encode('utf-8')
        # ... else:
        # ...     print type(category.__unicode__())
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
