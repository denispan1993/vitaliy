__author__ = 'user'

from django.db import models

class Manager(models.Manager):

    def published(self):
        return self.filter(visibility=True, ).order_by('-created_at')

    def first_level(self):
        return self.published().filter(parent__isnull=True, )