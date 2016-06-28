# -*- coding: utf-8 -*-
from apps.utils.captcha.views import key_generator
from apps.authModel.models import Email
from apps.cart.models import Order
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

__author__ = 'AlexStarov'


class MailAccount(models.Model, ):
    is_active = models.BooleanField(verbose_name=_(u'Аккаунт активный', ),
                                    blank=False,
                                    null=False,
                                    default=True, )
    is_auto_active = models.BooleanField(verbose_name=_(u'Аккаунт автоматически активный', ),
                                         blank=False,
                                         null=False,
                                         default=True, )
    auto_active_datetime = models.DateTimeField(verbose_name=_(u'Дата закрытия аккаунта',),
                                                blank=False,
                                                null=False,
                                                default=datetime.now, )
    email = models.CharField(verbose_name=_(u'E-Mail', ),
                             max_length=64,
                             blank=False,
                             null=False, )
    server = models.ForeignKey(verbose_name=_(u'SMTP Server', ),
                               to='MailServer',
                               blank=False,
                               null=False, )
    username = models.CharField(verbose_name=_(u'UserName - login', ),
                                max_length=64,
                                blank=False,
                                null=False, )
    password = models.CharField(verbose_name=_(u'User password', ),
                                max_length=64,
                                blank=False,
                                null=False, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
                                      # default=datetime.now(), )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )
                                      #default=datetime.now(), )

    @property
    def get_provider(self):
        return self.email.split('@')[1]

    @property
    def get_return_path_subscribe(self):
        return 'subscribe@{0}'.format(self.get_provider, )


    # @property
    # def is_active(self):
    #     return self.server.is_active

    def __unicode__(self):
        return u'%s -> %s:%d' % (self.email, self.server.server, self.server.port, )

    class Meta:
        db_table = 'MailAccount'
        ordering = ['-created_at', ]
        get_latest_by = 'pk'
        verbose_name = u'SMTP Account'
        verbose_name_plural = u'SMTP Accounts'


class MailServer(models.Model, ):
    is_active = models.BooleanField(verbose_name=_(u'Сервер активный', ),
                                    blank=False,
                                    null=False,
                                    default=True, )
    server = models.CharField(verbose_name=_(u'SMTP Server', ),
                              max_length=64,
                              blank=False,
                              null=False, )
    port = models.PositiveSmallIntegerField(verbose_name=_(u'SMTP Port', ),
                                            blank=True,
                                            null=True,
                                            default=25, )
    use_tls = models.BooleanField(verbose_name=_(u'Use TLS', ),
                                  default=True, )
    use_ssl = models.BooleanField(verbose_name=_(u'Use SSL', ),
                                  default=False, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
                                      # default=datetime.now(), )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )
                                      # default=datetime.now(), )

    def __unicode__(self):
        return u'%s:%d' % (self.server, self.port, )

    class Meta:
        db_table = 'MailServer'
        ordering = ['-created_at', ]
        verbose_name = u'SMTP Server'
        verbose_name_plural = u'SMTP Servers'


def datetime_in_iso_format():
    return datetime.now().isoformat()


class Delivery(models.Model, ):
    name = models.CharField(verbose_name=_(u'Имя рассылки', ),
                            max_length=128,
                            blank=True,
                            null=True,
                            default=datetime_in_iso_format, )
    Type_Mailings = (
        (1, _(u'Фэйк рассылка', ), ),
        (2, _(u'Акция', ), ),
        (3, _(u'Новинки', ), ),
        (4, _(u'Рассылка на "SPAM" адреса', ), ),
        # (2, _(u'Под заказ', ), ),
        # (3, _(u'Ожидается', ), ),
        # (4, _(u'Недоступен', ), ),
    )
    delivery_test = models.BooleanField(verbose_name=_(u'Тестовая рассылка', ),
                                        blank=True,
                                        null=False,
                                        default=True, )
    send_test = models.BooleanField(verbose_name=_(u'Тестовая рассылка отослана', ),
                                    blank=True,
                                    null=False,
                                    default=True, )
    send_spam = models.BooleanField(verbose_name=_(u'SPAM рассылка отослана', ),
                                    blank=True,
                                    null=False,
                                    default=False, )
    send_general = models.BooleanField(verbose_name=_(u'Главная рассылка отослана', ),
                                       blank=True,
                                       null=False,
                                       default=True, )
    type = models.PositiveSmallIntegerField(verbose_name=_(u'Тип рассылки'),
                                            choices=Type_Mailings,
                                            default=1,
                                            blank=False,
                                            null=False, )
    subject = models.CharField(verbose_name=_(u'Subject рассылки', ),
                               max_length=256,
                               blank=True,
                               null=True, )
    html = models.TextField(verbose_name=_(u'Html текст рассылки "СЫРОЙ"', ),
                            blank=True,
                            null=True, )
    real_html = models.TextField(verbose_name=_(u'Html текст рассылки', ),
                                 blank=True,
                                 null=True, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
                                      # default=datetime.now(), )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )
                                      # default=datetime.now(), )

    # Вспомогательные поля
    img = generic.GenericRelation('Email_Img',
                                  content_type_field='content_type',
                                  object_id_field='object_id', )

    def save(self, *args, **kwargs):
        real_html = self.html
        def_str1 = u'<figure><p><img src='
        def_str2 = u'</figure>'
        while def_str1 in real_html:
            try:
                val_begin = real_html.index(def_str1)
            except ValueError:
                break
            else:
                pass
            try:
                val_end = real_html.index(def_str2)
            except ValueError:
                break
            else:
                val_end += 9
            real_html = u'%s%s' % (real_html[:val_begin], real_html[val_end:], )
        img = self.img.all()
        if img.count() > 0:
            for i in range(1, img.count()+1, ):
                def_str = u'{{ фото:%.1d }}' % i
                if def_str in real_html:
                    img_aaa = img[i-1].img
                    #old_name = img[i-1].img.name
                    thumb_size = ((img[i-1].height, img[i-1].width, ), )
                    #file_name = img_aaa.name.rsplit('/', 1, )[1]
                    #file_format = file_name.rsplit('.', 1, )[1]
                    img_aaa.field.sizes = thumb_size
                    #img_aaa.save(name=file_name,
                    #             content=generate_thumb(img=img_aaa,
                    #                                    thumb_size=thumb_size[0],
                    #                                    format=file_format, ), )
                    #img_url = 'img_aaa.url_%dx%d' % (img[i-1].height, img[i-1].width, )
                    #img_url = eval(img_url,
                    #               {'__builtins__': {}, },
                    #               {'img_aaa': img_aaa, }, )
                    img_url = img_aaa.url.rsplit('.', 1, )
                    img_url = '%s_%dx%d.%s' % (img_url[0], img[i-1].height, img[i-1].width, img_url[1], )
                    from django.template.loader import render_to_string
                    link_str = render_to_string('render_img_string.jinja2.html',
                                                {'imgN': def_str,
                                                 'img_url': img_url,
                                                 'alt': img[i-1].meta_alt,
                                                 'title': img[i-1].title,
                                                 'caption': img[i-1].sign, }, )
                    #value = eval(string,
                    #     {'__builtins__': {}, },
                    #     {'variable_set': variable_set, }, )
                    real_html = real_html.replace(def_str, link_str, )
                    #try:
                    #    img_aaa.storage.delete(old_name, )
                    #except:
                    #    pass

        self.real_html = real_html
        super(Delivery, self).save(*args, **kwargs)  # Call the "real" save() method.

    @property
    def emails_delivered(self):
        EmailMiddleDelivery_all = EmailMiddleDelivery.objects.filter(delivery=self,
                                                                     delivery_test_send=False,
                                                                     spam_send=False,
                                                                     delivery_send=True, ).values_list('pk', flat=True, )
        if len(EmailMiddleDelivery_all, ) < 1:
            EmailMiddleDelivery_all = EmailMiddleDelivery.objects.filter(delivery=self,
                                                                         delivery_test_send=False,
                                                                         spam_send=True,
                                                                         delivery_send=False, ).values_list('pk', flat=True, )
        i = 0
        if not EmailMiddleDelivery_all == []:
            i += EmailForDelivery.objects.filter(delivery_id__in=EmailMiddleDelivery_all, ).count()
        return i

    @property
    def trace_of_visits(self):
        return TraceOfVisits.objects.filter(delivery=self, )\
            .exclude(email__delivery__delivery_test_send=True, )\
            .count()

    @property
    def trace_of_visits_unique(self):
        return TraceOfVisits.objects.filter(delivery=self, )\
            .exclude(email__delivery__delivery_test_send=True, )\
            .values('email__content_type', 'email__object_id', )\
            .distinct()\
            .count()

    @property
    def order_from_trace_of_visits(self):
        trace_of_visits = TraceOfVisits.objects.filter(delivery=self, )\
            .exclude(email__delivery__delivery_test_send=True, )
        unique_trace_email_pk = []
        for trace in trace_of_visits:
            trace_email_pk = trace.email.now_email.pk
            if trace_email_pk not in unique_trace_email_pk:
                unique_trace_email_pk.append(trace_email_pk, )
        #from datetime import timedelta
        #delta = timedelta(days=100, )
        unique_orders = []
        for trace_pk in unique_trace_email_pk:
            try:
                this_trace = trace_of_visits.get(pk__in=trace_pk, )
            except TraceOfVisits.DoesNotExist:
                continue
            else:
                try:
                    order = Order.objects.get(email=this_trace.email.now_email.email, )
                                              # created_at__lte=this_trace.cteated_at + delta, )
                except Order.DoesNotExist:
                    continue
                except Order.MultipleObjectsReturned:
                    unique_orders.append(1, )
                else:
                    unique_orders.append(order.pk, )

        return len(unique_orders, )

    @property
    def emails(self):
        from apps.authModel.models import Email
        return Email.objects.count()

    @property
    def images(self):
        return self.img.all().order_by('pk', )

    @property
    def bad_emails(self):
        from apps.authModel.models import Email
        return Email.objects.filter(bad_email=True, ).count()

    @property
    def text_type(self):
        return self.Type_Mailings[self.type-1][1]

    @property
    def get_url_number(self):
        return '%06d' % self.id

    @models.permalink
    def get_absolute_url(self, ):
        return ('admin_delivery:edit',
                (),
                {'delivery_id': self.get_url_number, }, )
#                {'delivery_id': '%06d' % self.pk, }, )

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
        return u'Рассылка: № %6d - %s' % (self.pk, self.name, )

#    def save(self, *args, **kwargs):
#        from django.utils.timezone import now
#        if not self.created_at:
#            self.created_at = now()
#        self.updated_at = now()
#        return super(CouponGroup, self).save(*args, **kwargs)

    class Meta:
        db_table = 'Delivery'
        ordering = ['-created_at', ]
        verbose_name = u'Рассылка'
        verbose_name_plural = u'Рассылки'


def set_path_photo(self, filename):
    return 'email_img/%.6d/%s' % (
        # self.product.pub_datetime.year,
        self.object_id,
        filename)
def set_path_img(self, filename):
    return 'email_img/%.6d/%s' % (
        # self.product.pub_datetime.year,
        self.object_id,
        filename)


class Email_Img(models.Model):
    from django.contrib.contenttypes.models import ContentType
    content_type = models.ForeignKey(ContentType, related_name='related_Email_Img', )
    object_id = models.PositiveIntegerField(db_index=True, )
    from django.contrib.contenttypes import generic
    parent = generic.GenericForeignKey('content_type', 'object_id', )

    name = models.CharField(verbose_name=_(u'Наименование картинки', ),
                            max_length=256,
                            null=True,
                            blank=True, )

    tag_name = models.CharField(verbose_name=_(u"Имя tag'a картинки", ),
                                max_length=8,
                                null=True,
                                blank=True,
                                help_text=_(u'TAG картинки не может быть длинее 8 символов,'
                                            u' только английские маленькие буквы и цифры'
                                            u' без пробелов и подчеркиваний', ), )

    from compat.ImageWithThumbs import models as class_ImageWithThumb
    image = class_ImageWithThumb.ImageWithThumbsField(verbose_name=u'Картинка',
                                                      upload_to=set_path_img,
                                                      sizes=((26, 26, ), (50, 50, ), (90, 95, ),
                                                             (205, 190, ), (210, 160, ), (345, 370, ),
                                                             (700, 500, ), ),
                                                      blank=False,
                                                      null=False, )
    #Дата создания и дата обновления новости. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Картинка для E-Mail: %s' % (self.name, )

    class Meta:
        db_table = 'EMail_Img'
        ordering = ['-created_at', ]
        verbose_name = "Картинка для E-Mail"
        verbose_name_plural = "Картинкии для E-Mail"


class EmailMiddleDelivery(models.Model, ):
    delivery = models.ForeignKey(to=Delivery,
                                 verbose_name=_(u'Указатель на рассылку', ),
                                 blank=False,
                                 null=False, )
    delivery_test_send = models.BooleanField(verbose_name=_(u'Тестовая рассылка - отослана', ),
                                             blank=True,
                                             null=False,
                                             default=True, )
    spam_send = models.BooleanField(verbose_name=_(u'SPAM рассылка - отослана', ),
                                    blank=True,
                                    null=False,
                                    default=True, )
    delivery_send = models.BooleanField(verbose_name=_(u'Рассылка - отослана', ),
                                        blank=True,
                                        null=False,
                                        default=True, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
                                      # default=datetime.now(), )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )
                                      # default=datetime.now(), )

    def __unicode__(self):
        return u'Промежуток рассылки: № %6d - %s, Test: %s, Send: %s, created_at: %s, updated_at: %s'\
               % (self.pk, self.delivery.name, self.delivery_test_send, self.delivery_send,
                  self.created_at, self.updated_at, )

    class Meta:
        db_table = 'EmailMiddleDelivery'
        ordering = ['-created_at', ]
        verbose_name = u'Промежуточная можель Рассылки'
        verbose_name_plural = u'Промежуточные можели Рассылок'


class EmailForDelivery(models.Model, ):
    delivery = models.ForeignKey(to=EmailMiddleDelivery,
                                 verbose_name=_(u'Указатель на рассылку', ),
                                 blank=False,
                                 null=False, )
    key = models.CharField(verbose_name=_(u'ID E-Mail адреса и рассылки', ),
                           max_length=8,
                           blank=False,
                           null=False,
                           # unique=True, )
                           default=key_generator, )
    email = models.ForeignKey(to=Email,
                              verbose_name=_(u'E-Mail', ),
                              blank=True,
                              null=True, )
    content_type = models.ForeignKey(ContentType,
                                     related_name='email_instance',
                                     verbose_name=_(u'Указатель на E-Mail', ),
                                     blank=True,
                                     null=True, )
    object_id = models.PositiveIntegerField(db_index=True,
                                            blank=True,
                                            null=True, )
    now_email = generic.GenericForeignKey('content_type', 'object_id', )

    send = models.BooleanField(verbose_name=_(u'Флаг отсылки', ),
                               blank=True,
                               null=False,
                               default=False, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True, )

    def save(self, *args, **kwargs):
        if not self.pk:
            while True:
                key = key_generator()
                try:
                    EmailForDelivery.objects.get(key=key, )
                except EmailForDelivery.DoesNotExist:
                    self.key = key
                    break
                except IntegrityError:
                    print 'IntegrityError Key: %s' % key
                except Exception as e:
                    print 'Exception type: %s, message: %s' % (type(e, ), e, )
        super(EmailForDelivery, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'E-Mail: %s pk: %6d created_at: %s, updated_at: %s'\
               % (self.now_email.email, self.pk, self.created_at, self.updated_at, )

    class Meta:
        db_table = 'EmailForDelivery'
        ordering = ['-created_at', ]
        verbose_name = u'Рассылка (Email адрес)'
        verbose_name_plural = u'Рассылки (Email адреса)'


class TraceOfVisits(models.Model, ):
    delivery = models.ForeignKey(to=Delivery,
                                 verbose_name=_(u'Указатель на рассылку', ),
                                 blank=False,
                                 null=False, )
    email = models.ForeignKey(to=EmailForDelivery,
                              verbose_name=_(u'Указатель на E-Mail пользователя', ),
                              blank=False,
                              null=False, )
    sessionid = models.CharField(verbose_name=u'SessionID',
                                 max_length=32,
                                 blank=True,
                                 null=True,
                                 default=0, )
    url = models.CharField(verbose_name=_(u'URL переадресации', ),
                           max_length=255,
                           blank=True,
                           null=True, )
    target = models.CharField(verbose_name=_(u'Цэль захода на сайт'),
                              max_length=32,
                              blank=True,
                              null=True, )
    target_id = models.PositiveSmallIntegerField(verbose_name=_(u'Тип цэли захода на сайт'),
                                                 blank=True,
                                                 null=True, )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
                                      # default=datetime.now(), )

    @property
    def delivery_fk(self):
        return self.delivery.name

    @property
    def email_fk(self):
        if self.email.now_email:
            return self.email.now_email.email
        if self.email:
            return self.email.now_email

    @property
    def email_fk_key(self):
        return self.email.key

    class Meta:
        db_table = 'TraceOfVisits'
        ordering = ['-created_at', ]
        verbose_name = u'След от посещения'
        verbose_name_plural = u'Следы от посещений'


class SpamEmail(models.Model, ):
    email = models.EmailField(verbose_name=_(u'E-Mail', ),
                              blank=False,
                              null=False, )
    # Рассылка Спам
    delivery_spam = models.BooleanField(verbose_name=_(u'Спам', ),
                                        default=True, )
    # Рассылка новых продуктов
    delivery_new_products = models.BooleanField(verbose_name=_(u'Новые продукты', ),
                                                default=True, )
    # Рассылка акций и новостей
    delivery_shares_news = models.BooleanField(verbose_name=_(u'Новости и Акции', ),
                                               default=True, )
    bad_email = models.BooleanField(verbose_name=_(u'Bad E-Mail', ),
                                    default=False, )
    # Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    @property
    def content_type(self, ):
        from django.contrib.contenttypes.models import ContentType
        return ContentType.objects.get_for_model(model=self, for_concrete_model=True, )

    class Meta:
        db_table = 'SpamEmail'
        ordering = ['-created_at', ]
        verbose_name = u'Емэйл для спама'
        verbose_name_plural = u'Емэйлы для спама'
