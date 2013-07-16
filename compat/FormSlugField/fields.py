# coding=utf-8
__author__ = 'Sergey'

from django.db import models
from django.utils.translation import ugettext as _
#from south.modelsinspector import add_introspection_rules

#================================
#from django.utils.translation import ugettext_lazy as _
#from django.db import models
import re

#from compat.ruslug.forms import RuSlugFormField

from django.forms import CharField #as FormCharField
#from django.core import validators
from django.core.validators import RegexValidator

# slug_re = re.compile(r'^[-a-zA-Zа-яА-ЯёЁіІїЇґҐєЄ0-9_.]+$')
# slug_re = re.compile(r'^[-a-zA-Zа-яА-ЯёЁіІїЇґҐєЄ0-9_.]+$', re.U, )
slug_re = re.compile(r'^[-\w]+$', re.U)

validate_slug = RegexValidator(slug_re, _("Enter a valid 'slug' consisting of letters, numbers,"
                                          " underscores or hyphens."),
                               'invalid', )


#class FormSlugField(FormCharField, ):
class FormSlugField(CharField, ):
    default_error_messages = {
        'invalid': _("Enter a valid 'slug' consisting of letters, numbers,"
                     " underscores or hyphens.", ),
        }
#    default_validators = [validators.validate_slug]
    default_validators = [validate_slug, ]

#    class media:
#        js = ('/media/js/admin/ruslug-urlify.js', )

#class RuSlugField(models.CharField, ):
#    def formfield(self, **kwargs):
#        defaults = {
#            'form_class': RuSlugFormField,
#            'error_messages': {
#                'invalid': _(u"Enter a valid 'slug' consisting of letters, numbers,"
#                             u" underscores or hyphens."),
#                }
#        }
#        defaults.update(kwargs)
#        return super(RuSlugField, self).formfield(**defaults)
#===================================================================================
