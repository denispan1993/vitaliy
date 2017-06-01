# -*- coding: utf-8 -*-
__author__ = 'user'

from django.db import models


class Manager(models.Manager):

    def pass_moderation(self):
        return self.filter(pass_moderation=True, )
