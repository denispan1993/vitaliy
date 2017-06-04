# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime

__author__ = 'AlexStarov'


class Manager(models.Manager):

    def location_date_time_gte_today(self):
        aaa = self.location_date_time.filter(date_start__gte=datetime.today(), )
        print(self, )
        print(aaa, )
        return aaa

    def published(self):
        return self.filter(visibility=1, ).order_by('-created_at')

    def first_level(self):
        return self.published().filter(parent__isnull=1, )


#    # Закрепленные в рубриках
#    def rubric_locked(self, rubric=None):
#        qs = self.published()
#        if rubric:
#            try:
#                return qs.get(rubric_locked=1, rubric=rubric)
#            except self.model.DoesNotExist:
#                return None
#        else:
#            qs = qs.filter(rubric_locked=1, first_locked=0)
#            return qs

