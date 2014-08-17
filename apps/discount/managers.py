# -*- coding: utf-8 -*-
__author__ = 'user'

from django.db import models
from datetime import datetime


class Manager_Action(models.Manager, ):

    def not_deleted(self):
        return self.filter(auto_del=False, )

    def active(self):
        return self.not_deleted().filter(datetime_start__lte=datetime.now(),
                                         datetime_end__gte=datetime.now(), )
