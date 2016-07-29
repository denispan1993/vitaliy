# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slide', '0003_auto_20160517_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='opening_method',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='\u041c\u0435\u0442\u043e\u0434 \u043e\u0442\u043a\u0440\u044b\u0442\u0438\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b \u0441\u043b\u0430\u0439\u0434\u0430', choices=[(1, b'_blank'), (2, b'_self')]),
        ),
        migrations.AddField(
            model_name='slide',
            name='url',
            field=models.CharField(max_length=256, null=True, verbose_name='Url', blank=True),
        ),
    ]
