# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime
from django.db.models import Q

__author__ = 'AlexStarov'


class Manager_Action(models.Manager, ):

    def not_deleted(self):
        return self.filter(deleted=False, )

    def active(self):
        return self.not_deleted().filter(Q(datetime_start__lte=datetime.now(), ),
                                         Q(datetime_end__gte=datetime.now(), ), )

    def not_active(self):
        return self.not_deleted().filter(Q(datetime_start__gt=datetime.now(), ) |
                                         Q(datetime_end__lt=datetime.now(), ), )
