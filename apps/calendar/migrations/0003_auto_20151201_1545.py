# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('calendar', '0002_auto_20151201_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationdatetime',
            name='time_end',
            field=models.TimeField(default=datetime.time(13, 45, 29, 389082), verbose_name='\u0412\u0440\u0435\u043c\u044f \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f \u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='locationdatetime',
            name='time_start',
            field=models.TimeField(default=datetime.time(13, 45, 29, 388998), verbose_name='\u0412\u0440\u0435\u043c\u044f \u043d\u0430\u0447\u0430\u043b\u0430 \u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u044f'),
        ),
    ]
