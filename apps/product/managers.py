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
        return self.visible().order_by('-created_at')

    def basement(self):
        return self.visible().filter(parent__isnull=True, )


class Manager_Product(models.Manager):

    def published(self, ):
        return self.filter(visibility=True, ).order_by('-created_at')

    def in_main_page(self, ):
        self.published().filter(in_main_page=True, )


#    # Все опубликованные новости
#
#    def published(self):
##        self = self.select_related() # .select_related(depth=2)
#        return self.filter(published=1).order_by('-pub_date')

#    # Закрепленная на главной.
#    # Всегда нужно проверять на None
#    def first_locked(self):
#        from django.core.cache import cache
#        # try to get product from cache
#        first_locked = cache.get(u'first_locked', )
#        # if a cache miss, fall back on db query
#        if not first_locked:
#            try:
#                first_locked = self.published().get(first_locked=1, )
#            except self.model.DoesNotExist:
#                return None
#            # store item in cache for next time
#            else:
#                cache.set(u'first_locked', first_locked, 900, ) # 1h
#                return first_locked
#        else:
#            return first_locked

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
