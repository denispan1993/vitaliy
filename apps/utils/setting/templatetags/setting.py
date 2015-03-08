# -*- coding: utf-8 -*-
#from libxml2mod import name
__author__ = 'AlexStarov'

from django_jinja.library import Library

register = Library()

variable_types = {'char', 'text', 'integer', 'positivesmallinteger', 'img', }


@register.global_function(name='get_value_variable', )
def get_value_variable(variable_name, variable_type, ):
    value = 'None'
    variable_type = variable_type.lower()
    from apps.utils.setting.models import Setting
    try:
        variable_set = Setting.objects.get(variable_name=variable_name, )
    except Setting.DoesNotExist:
        variable_set = None
        value = 'value of %s variable_name, variable_type is %s is None' % (variable_name, variable_type, )
    else:
        if variable_type == 'img':
            """ Получаем запись непосредственно на запись в базе данных на нашу картинку """
            string = 'variable_set.%s.all()[0]' % variable_type
            value = eval(string,
                         {'__builtins__': {}, },
                         {'variable_set': variable_set, }, )
            return value.photo,\
                   value.photo.path,\
                   value.photo.url
                   # value.photo.url.split('/media', 1, )[1]  # Почему-то путь выводится с дополнительным /media
                   #                                          # нам нужно его обрезать.
        if variable_type in variable_types:
            #string = "value = variable_set.%s" % variable_type
            #exec string
            string = 'variable_set.%s' % variable_type
            #  eval("(lambda:0).func_code", {'__builtins__':{}})
            value = eval(string,
                         {'__builtins__': {}, },
                         {'variable_set': variable_set, }, )
    return value
