# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mycalendar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationdatetime',
            name='date_end',
            field=models.DateField(default=datetime.date.today, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f \u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='locationdatetime',
            name='date_start',
            field=models.DateField(default=datetime.date.today, verbose_name='\u0414\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430 \u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='locationdatetime',
            name='time_end',
            field=models.TimeField(default=datetime.time(13, 40, 30, 195838), verbose_name='\u0412\u0440\u0435\u043c\u044f \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f \u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='locationdatetime',
            name='time_start',
            field=models.TimeField(default=datetime.time(13, 40, 30, 195748), verbose_name='\u0412\u0440\u0435\u043c\u044f \u043d\u0430\u0447\u0430\u043b\u0430 \u043c\u0435\u0440\u043e\u043f\u0440\u0438\u044f\u0442\u0438\u044f'),
        ),
    ]
