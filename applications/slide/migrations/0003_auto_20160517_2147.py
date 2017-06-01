# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import applications.slide.models


class Migration(migrations.Migration):

    dependencies = [
        ('slide', '0002_auto_20160507_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slide',
            name='name',
            field=models.CharField(default=applications.slide.models.default_slide_name, max_length=128, null=True, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0441\u043b\u0430\u0439\u0434\u0430', blank=True),
        ),
    ]
