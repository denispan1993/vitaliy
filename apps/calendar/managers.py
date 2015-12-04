# -*- coding: utf-8 -*-
__author__ = 'AlexStarov'
from django.db import models
from datetime import datetime


class Manager(models.Manager):

    def location_date_time__gte_today(self):
        return self.location_date_time.filter(date_start__gte=datetime.today(), ).distinct()

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

