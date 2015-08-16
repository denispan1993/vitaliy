# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


from datetime import date, datetime


def add_months(d, x, ):
    new_month = (((d.month - 1) + x) % 12) + 1
    new_year = d.year + (((d.month - 1) + x) / 12)
    import calendar
    new_day = min(d.day, calendar.monthrange(new_year, new_month, )[1], )
    return date(new_year, new_month, new_day, ) #d.hour, d.minute, d.second, d.microsecond,


def add_three_month():
    return add_months(date.today(), 3, )


class CouponGroup(models.Model, ):
    name = models.CharField(verbose_name=_(u'Имя группы купонов', ),
                            max_length=128,
                            blank=True,
                            null=True,
                            default=datetime.now().isoformat(), )
    how_much_coupons = models.PositiveSmallIntegerField(verbose_name=_(u'Количество сгенерированных купонов', ),
                                                        blank=True,
                                                        null=True,
                                                        default=10, )
    number_of_possible_uses = models.PositiveSmallIntegerField(verbose_name=_(u'Количество возможных использований', ),
                                                               blank=True,
                                                               null=True,
                                                               default=1, )
    percentage_discount = models.PositiveSmallIntegerField(verbose_name=_(u'Процент скидки', ),
                                                           blank=True,
                                                           null=True,
                                                           default=10, )
    start_of_the_coupon = models.DateTimeField(verbose_name=_(u'Врямя начала действия купонов', ),
                                               blank=True,
                                               null=True,
                                               default=date.today(), )
    end_of_the_coupon = models.DateTimeField(verbose_name=_(u'Врямя окончания действия купонов', ),
                                             blank=True,
                                             null=True,
                                             default=add_three_month(), )
    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(verbose_name=_(u'Дата создания', ),
                                      blank=True,
                                      null=True,
                                      default=datetime.now(), )
    updated_at = models.DateTimeField(verbose_name=_(u'Дата обновления', ),
                                      blank=True,
                                      null=True,
                                      default=datetime.now(), )

    def save(self, *args, **kwargs):
        from django.utils import timezone
        self.start_of_the_coupon.hour += 3
        self.end_of_the_coupon.hour += 3
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(CouponGroup, self).save(*args, **kwargs)

    #@models.permalink
    def get_absolute_url(self, ):
        return u'/админ/купон/группа/редактор/%.6d/' % self.pk
        # return ('admin_coupon:coupon_group_edit',
        #         {'coupon_group_id': self.pk, }, )

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
        return u'Группа купонов: № %6d - %s' % (self.pk, self.name, )

#    def save(self, *args, **kwargs):
#        from django.utils.timezone import now
#        if not self.created_at:
#            self.created_at = now()
#        self.updated_at = now()
#        return super(CouponGroup, self).save(*args, **kwargs)

    class Meta:
        db_table = 'CouponGroup'
        ordering = ['-created_at', ]
        verbose_name = u'Группа купонов'
        verbose_name_plural = u'Группы купонов'


class Coupon(models.Model, ):
    name = models.CharField(verbose_name=_(u'Имя купона', ),
                            max_length=128,
                            blank=True,
                            null=True,
                            default=datetime.now().isoformat(), )
    coupon_group = models.ForeignKey(to=CouponGroup,
                                     verbose_name=_(u'Группа купонов'),
                                     blank=True,
                                     null=True,
                                     help_text=u'Ссылка на групу купонов', )
    from apps.utils.captcha.views import key_generator
    from string import ascii_lowercase, digits
    key = models.CharField(verbose_name=_(u'Ключ купона', ),
                           unique=True,
                           max_length=8,
                           blank=False,
                           null=False,
                           default=key_generator(size=6, chars=ascii_lowercase + digits, ), )
    """
        Какой заказ создал этот купон.
    """
    from apps.cart.models import Cart, Order
    parent = models.ForeignKey(to=Order,
                               verbose_name=_(u'Заказ который создал этот купон', ),
                               blank=True,
                               null=True, )

    number_of_possible_uses = models.PositiveSmallIntegerField(verbose_name=_(u'Количество возможных использований', ),
                                                               blank=False,
                                                               null=False,
                                                               default=1, )
    number_of_uses = models.PositiveSmallIntegerField(verbose_name=_(u'Количество использований', ),
                                                      blank=False,
                                                      null=False,
                                                      default=0, )
    """
        Какие корзины и заказы использовали этот купон.
    """
    child_cart = models.ManyToManyField(to=Cart,
                                        related_name=u'Cart_child',
                                        verbose_name=_(u'Корзины которые использовали этот купон', ),
                                        blank=True,
                                        null=True, )
    child_order = models.ManyToManyField(to=Order,
                                         related_name=u'Order_child',
                                         verbose_name=_(u'Заказы которые использовали этот купон', ),
                                         blank=True,
                                         null=True, )
    percentage_discount = models.PositiveSmallIntegerField(verbose_name=_(u'Процент скидки', ),
                                                           blank=False,
                                                           null=False,
                                                           default=10, )
    start_of_the_coupon = models.DateTimeField(verbose_name=_(u'Врямя начала действия купона', ),
                                               blank=False,
                                               null=False,
                                               default=date.today(), )
    end_of_the_coupon = models.DateTimeField(verbose_name=_(u'Врямя окончания действия купона', ),
                                             blank=False,
                                             null=False,
                                             default=add_three_month(), )

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(verbose_name=_(u'Дата создания', ),
                                      blank=False,
                                      null=False,
                                      default=datetime.now(), )
    updated_at = models.DateTimeField(verbose_name=_(u'Дата обновления', ),
                                      blank=False,
                                      null=False,
                                      default=datetime.now(), )

    # from apps.comment import managers
    # objects = managers.Manager()

##    @models.permalink
#    def get_absolute_url(self, ):
##        return ('show_product', (),
##                {'product_url': self.url,
##                 'id': self.pk, }, )
#        # model = self.content_type.model_class()
#        # object = model.objects.get(pk=self.object_id, )
#        # url = object.get_absolute_url()
#        object = self.content_type.get_object_for_this_type(pk=self.object_id, )
#        url = object.get_absolute_url()
#        return u'%sкомментарий/%.6d/' % (url, self.pk, )

    #@staticmethod
    #@models.permalink
    def get_absolute_url(self, ):
        return u'/админ/купон/редактор/%.6d/' % self.pk
        # return ('admin_coupon:coupon_edit',
        #         (),  # (self.pk, ), )
        #         {'coupon_id': self.pk, }, )

#    get_url = property(get_absolute_url)

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
        return u'Coupon: %6d - %s' % (self.pk, self.name, )

    def save(self, *args, **kwargs):
        from django.utils.timezone import now
        if not self.created_at:
            self.created_at = now()
        self.updated_at = now()
        return super(Coupon, self).save(*args, **kwargs)

    class Meta:
        db_table = 'Coupon'
        ordering = ['-created_at', ]
        verbose_name = u'Купон'
        verbose_name_plural = u'Купоны'
