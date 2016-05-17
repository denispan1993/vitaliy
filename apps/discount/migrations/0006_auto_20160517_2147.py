# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import apps.discount.models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0005_auto_20160507_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='datetime_end',
            field=models.DateTimeField(default=apps.discount.models.default_datetime_end, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f \u0430\u043a\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='action',
            name='datetime_start',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430 \u0430\u043a\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='action',
            name='name',
            field=models.CharField(default=apps.discount.models.default_action_name, max_length=256, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0430\u043a\u0446\u0438\u0438'),
        ),
    ]
