# coding=utf-8
from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.


class Static(models.Model):
    order = models.PositiveSmallIntegerField(verbose_name=_(u'Порядок сортировки'),
                                             # visibility=True,
                                             db_index=True,
                                             unique=True,
                                             blank=True,
                                             null=True,
                                             help_text=u'Цифры от 1 до 99', )
    from compat.FormSlug import models as class_FormSlugField
    url = class_FormSlugField.ModelSlugField()
    title = models.CharField(verbose_name=u'Заголовок страницы',
                             max_length=255,
                             null=False,
                             blank=False, )
    text = models.TextField(verbose_name=u'Текст страницы',
                            null=True,
                            blank=True, )
    #Дата создания и дата обновления новости. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, )
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, )
    #Описание и ключевые слова для поисковиков
    meta_title = models.CharField(verbose_name=u'META заголовок страницы',
                                  max_length=190,
                                  null=True,
                                  blank=True,
                                  help_text=u'Данный заголовок читают поисковые системы для правильного'
                                            u' расположения страницы в поиске.', )
    meta_description = models.CharField(verbose_name=u'META описание',
                                        max_length=190,
                                        null=True,
                                        blank=True,
                                        help_text=u'Данное описание читают поисковые системы для правильного'
                                                  u' расположения страницы в поиске.', )
    meta_keywords = models.CharField(verbose_name=u'META клчевые слова',
                                     max_length=160,
                                     null=True,
                                     blank=True,
                                     help_text=u'Ключевые слова для поисковых систем.', )
    #Расширенные настройки
    template = models.CharField(verbose_name=u'Имя шаблона',
                                max_length=70,
                                null=True,
                                blank=True,
                                help_text=u'Пример: "news/reklama.html". Если не указано, система'
                                          u' будет использовать "news/default.html".', )
    visibility = models.BooleanField(verbose_name=u'Признак видимости категории', default=True, )

    def get_absolute_url(self, ):
#        return ('show_category', (),
#                {'category_url': unicode(str(self.url)),
#                 'id': unicode(str(self.pk)), }, )
        return u'/%s/' % self.url

    class Meta:
        db_table = 'Static_Pages'
        ordering = ['order', ]
        verbose_name = u'Статическая страница'
        verbose_name_plural = u'Статические страницы'
