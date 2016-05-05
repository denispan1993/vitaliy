# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycalendar', '0005_auto_20151201_1601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='location_date_time',
        ),
        migrations.AddField(
            model_name='event',
            name='location_date_time',
            field=models.ManyToManyField(default=1, to='mycalendar.LocationDateTime', verbose_name='\u041c\u0435\u0441\u0442\u043e \u0434\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u043f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0438\u044f'),
        ),
    ]
