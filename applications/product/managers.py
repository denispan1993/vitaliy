# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
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

        if not isinstance(kwargs.get('position', False), bool):
            position = kwargs.pop('position')

            if position == 0:
                category_key = 'category_basement'
            elif position == 1:
                category_key = 'category_basement_top'
            elif position == 2:
                category_key = 'category_basement_bottom'

        else:

            try:
                category_key = 'category_parent_pk_%d' % self._constructor_args[0][0].pk
            except IndexError:
                category_key = 'category_parent_pk_0'

        result = cache.get(key=category_key)
        if not isinstance(result, models.QuerySet):

            result = self.published(*args, **kwargs).order_by('serial_number', )
            cache.set(key=category_key,
                      value=result,
                      timeout=2400, )

        # from django import db
        # db.reset_queries()
        # print(len(db.connection.queries), db.connections['default'].queries[0])
        return result

    def basement(self, *args, **kwargs):
        return self.serial_number(parent__isnull=True, *args, **kwargs)

    def not_basement(self, *args, **kwargs):
        return self.serial_number(*args, **kwargs).filter(parent__isnull=False, )

    def category_column(self, q, order, *args, **kwargs):

        cache_key = 'category_column_%s' % order
        result = cache.get(key=cache_key)
        if not result:

            result = self.visible(q, *args, **kwargs).order_by(order, )

            cache.set(key=cache_key,
                      value=result,
                      timeout=1200, )

        return result

    def left_vertical_column(self, *args, **kwargs):
        return self.category_column(q=Q(serial_number_left_vertical_column__gt=0),
                                    order='serial_number_left_vertical_column', *args, **kwargs)

    def footer_column_first(self, *args, **kwargs):
        return self.category_column(q=Q(serial_number_first_column__gt=0),
                                    order='serial_number_first_column', *args, **kwargs)

    def footer_column_second(self, *args, **kwargs):
        return self.category_column(q=Q(serial_number_second_column__gt=0),
                                    order='serial_number_second_column', *args, **kwargs)

    def footer_column_third(self, *args, **kwargs):
        return self.category_column(q=Q(serial_number_third_column__gt=0),
                                    order='serial_number_third_column', *args, **kwargs)

    def footer_column_fourth(self, *args, **kwargs):
        return self.category_column(q=Q(serial_number_fourth_column__gt=0),
                                    order='serial_number_fourth_column', *args, **kwargs)


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
