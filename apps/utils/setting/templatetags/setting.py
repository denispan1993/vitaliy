__author__ = 'AlexStarov'

from django_jinja.library import Library

register = Library()


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
        string = "value = variable_set.%s" % variable_type
        exec string
    return value
