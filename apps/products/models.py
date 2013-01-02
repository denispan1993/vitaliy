from django.db import models

# Create your models here.

class Category(models.Model):
    parent = models.ForeignKey(u'self', verbose_name=u'Вышестоящая категория',
        related_name=u'children', null=True, blank=True, )
    title = models.CharField(verbose_name=u'Заголовок категории', max_length=256,
        null=False, blank=False, )
    name = models.CharField(verbose_name=u'Наименование категории', max_length=256,
        null=True, blank=True, )
    description = models.TextField(verbose_name=u'Описание категории',
        null=True, blank=True, )

    #Дата создания и дата обновления новости. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    #Описание и ключевые слова для поисковиков
    meta_title = models.CharField(verbose_name=u'Заголовок категории', max_length=190,
        null=True, blank=True,
                                  help_text=u'Данный заголовок читают поисковые системы для правильного расположения страницы в поиске.', )
    meta_description = models.CharField(verbose_name=u'Описание категории', max_length=190,
        null=True, blank=True,
                                   help_text=u'Данное описание читают поисковые системы для правильного расположения страницы в поиске.', )
    meta_keywords = models.CharField(verbose_name=u'Клчевые слова категории', max_length=160,
        null=True, blank=True,
                                help_text=u'Ключевые слова для поисковых систем.', )
    #Расширенные настройки
    template = models.CharField(verbose_name=u'Имя шаблона', max_length=70,
        null=True, blank=True,
                                help_text=u'Пример: "news/reklama.html". Если не указано, система будет использовать "news/default.html".', )
    visibility = models.BooleanField(verbose_name=u'Признак видимости категории', default=True, )

#    question = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')

#    def get_absolute_url(self, ):
#        return '/news/rubric/%s/' % self.url

    def __unicode__(self):
        return u'Категория:%s' % (self.title, )

    class Meta:
        db_table = 'Category'
        ordering = ['-created_at']
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
