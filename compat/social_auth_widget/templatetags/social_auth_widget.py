# from django import template
from django_jinja.library import Library
from django.conf import settings

register = Library()

@register.global_function()
def social_auth_widget():
    context ={'providers': settings.SOCIAL_AUTH_PROVIDERS, }
    from django.template.loader import render_to_string
    return render_to_string(template_name=u'social_auth_widget.jinja2.html', dictionary=context, )

#    return {
#        'providers': settings.SOCIAL_AUTH_PROVIDERS,
#    }


# register = template.Library()
# register.inclusion_tag('social_auth_widget.jinja2.html')(social_auth_widget)
