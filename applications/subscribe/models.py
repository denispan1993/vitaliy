# coding=utf-8
from django.db import models
# Create your models here.


class NewsLetter(models.Model):
    """
    Информационный бюлютень
    """

    #Дата создания и дата обновления. Устанавливаются автоматически.
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def __unicode__(self):
        return u'Корзина пользователя:%s, session:%s' % (self.user, self.sessionid, )  # self.session.session_key, )

    class Meta:
        db_table = u'Cart'
        ordering = [u'-created_at']
        verbose_name = u'Корзина'
        verbose_name_plural = u'Корзины'
