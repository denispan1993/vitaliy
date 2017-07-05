# -*- coding: utf-8 -*-
from django.db import models
from django.core.cache import cache

__author__ = 'AlexStarov'


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


class ManagerCategory(models.Manager):

    def visible(self, *args, **kwargs):
        return self.filter(visibility=True, is_active=True, *args, **kwargs)

    def published(self, *args, **kwargs):
        return self.visible(*args, **kwargs).order_by('-created_at', )

    def serial_number(self, *args, **kwargs):
        from django import db
        db.reset_queries()
        from django.core.cache import cache

        #print('self: ', self.__doc__, self.__dict__, )

        try:
            category_parent_pk = 'category_parent_pk_%d' % self._constructor_args[0][0].pk
        except IndexError:
            category_parent_pk = 'category_parent_pk_0'
        #print(category_parent_pk)
        result = cache.get(key=category_parent_pk)
        if not result:
            result = self.published(*args, **kwargs).order_by('serial_number', )
            #print('cache.set: ', result, )
            cache.set(key=category_parent_pk,
                      value=result,
                      timeout=600, )

        # print(len(db.connection.queries), db.connections['default'].queries[0])
        # print('result: ', result)
        return result

    def basement(self, *args, **kwargs):
        return self.serial_number(*args, **kwargs).filter(parent__isnull=True, )

    def not_basement(self, *args, **kwargs):
        return self.serial_number(*args, **kwargs).filter(parent__isnull=False, )


class ManagerProduct(models.Manager):

    def published(self, *args, **kwargs):
        return self.filter(visibility=True, *args, **kwargs).order_by('-created_at')

    def not_in_action(self, *args, **kwargs):
        return self.published().filter(in_action=False, *args, **kwargs)

    def in_action(self, *args, **kwargs):
        return self.published().filter(in_action=True, *args, **kwargs)

#    def recomendation(self, ):
#        return self.recomendate.filter(is_availability=1, ).order_by('-created_at')

#    def availability(self, ):
#        return self.filter(is_availability=1, ).order_by('-created_at')

    def in_main_page(self, limit=12, no_limit=False, ):
        # try to get product from cache
        in_main_page = cache.get(u'in_main_page', None, )
        # if a cache miss, fall back on db query
        if not in_main_page:
            try:
                if no_limit:
                    in_main_page = self.published().filter(in_main_page=True, )
                else:
                    in_main_page = self.published().filter(in_main_page=True, )[:limit]
                cache.set(u'in_main_page', in_main_page, 300, )  # 5 min

            except self.model.DoesNotExist:
                pass

        return in_main_page

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
