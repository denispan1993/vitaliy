# coding=utf-8
__author__ = 'user'
from django.db import models


class ManagerSlide(models.Manager):

    def visible(self):
        return self.filter(is_active=True, ).order_by('order', )


class ManagerRecommend(models.Manager):

    def visible(self):
        return self.filter(is_active=True, ).order_by('?', )
