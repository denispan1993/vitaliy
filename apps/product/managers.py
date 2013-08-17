__author__ = 'user'

from django.db import models

#class Manager(models.Manager):
#    pass

#    def published(self):
#        return self.filter(visibility=1, ).order_by('-created_at')

#    def first_level(self):
#        return self.published().filter(parent__isnull=1, )

#from django.db import models

#class Manager(models.Manager):

#    def published(self):
#        return self.filter(visibility=1, ).order_by('-created_at')


class Manager_Category(models.Manager):

    def visible(self):
        return self.filter(visibility=True, )

    def published(self):
        return self.filter(visibility=True, ).order_by('-created_at')

    def basement(self):
        return self.filter(visibility=True, parent__isnull=True, )


class Manager_Product(models.Manager):

    def published(self):
        return self.filter(visibility=True, ).order_by('-created_at')
