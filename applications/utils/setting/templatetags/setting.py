# -*- coding: utf-8 -*-
from django_jinja.library import global_function
from django.core.cache import cache

from applications.utils.setting.models import Setting

__author__ = 'AlexStarov'

variable_types = {'char', 'text', 'integer', 'positivesmallinteger', 'img', }


@global_function(name='get_value_variable', )
def get_value_variable(variable_name, variable_type, ):
    value = 'None'
    variable_type = variable_type.lower()
    try:
        variable_set = cache.get(key='variable_set_%s' % variable_name, )
        if not variable_set:
            variable_set = Setting.objects.get(variable_name=variable_name, )
            cache.set(
                key='variable_set_%s' % variable_name,
                value=variable_set,
                timeout=3600, )  # 60 sec * 60 min

        if variable_type == 'img':
            """ Получаем запись непосредственно на запись в базе данных на нашу картинку """

            value = eval('variable_set.%s.all()[0]' % variable_type,
                         {'__builtins__': {}, },
                         {'variable_set': variable_set, }, )

            return value.photo,\
                   value.photo.path,\
                   value.photo.url

        if variable_type in variable_types:

            string = 'variable_set.%s' % variable_type
            return eval(string,
                        {'__builtins__': {}, },
                        {'variable_set': variable_set, }, )

    except Setting.DoesNotExist:

        if variable_type is 'img':
            return None
        else:
            return 'value of %s variable_name, variable_type is %s is None' % (variable_name, variable_type, )
