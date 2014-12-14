__author__ = 'AlexStarov'

from django_jinja.library import Library

register = Library()

variable_types = ('char', 'text', 'integer', 'positivesmallinteger', 'img', )


@register.global_function(name='get_value_variable', )
def get_variable(variable_name, variable_type, ):
    value = 'None'
    from apps.utils.setting.models import Setting
    try:
        variable_set = Setting.objects.get(variable_name=variable_name, )
    except Setting.DoesNotExist:
        variable_set = None
        value = 'variable_set_None'
    else:
        if variable_type == 'img':
            return 'url', 'title', 'alt'
        elif variable_type in variable_types:
            # string = "value = variable_set.%s" % variable_type
            # exec string
            string = 'variable_set.%s' % variable_type
            #  eval("(lambda:0).func_code", {'__builtins__':{}})
            value = eval(string,
                         {'__builtins__': {}, },
                         {'variable_set': variable_set, }, )
    return value
