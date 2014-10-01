# -*- coding: utf-8 -*-
__author__ = 'Sergey'
from django.db import models
from django.utils.translation import ugettext_lazy as _


from compat.FormSlug.fields import FormSlugField


class ModelSlugField(models.CharField, ):
    description = _("Slug (up to %(max_length)s)")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 50, )
        # Set db_index=True unless it's been set manually.
        if 'db_index' not in kwargs:
            kwargs['db_index'] = True
        super(ModelSlugField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "SlugField"

    def formfield(self, **kwargs):
        defaults = {'form_class': FormSlugField, }
        defaults.update(kwargs)
        return super(ModelSlugField, self).formfield(**defaults)

# описываем правила
rules = [
    (
        (ModelSlugField, ), [],
        {
            "null": ["null", {"default": False}],
            "blank": ["blank", {"default": False}],
        }
    ),
]
# добавляем правила и модуль
from south.modelsinspector import add_introspection_rules
add_introspection_rules(rules, ["^compat\.FormSlug\.models\.ModelSlugField"])
