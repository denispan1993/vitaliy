# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0004_auto_20160505_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='datetime_end',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 14, 21, 45, 36, 167560), verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f \u0430\u043a\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='action',
            name='datetime_start',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 7, 21, 45, 36, 167503), verbose_name='\u0414\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430 \u0430\u043a\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='action',
            name='name',
            field=models.CharField(default='\u0410\u043a\u0446\u0438\u044f \u043e\u0442 2016-05-07 21:45:36.167403', max_length=256, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0430\u043a\u0446\u0438\u0438'),
        ),
    ]
