# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20151201_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='region',
        ),
        migrations.RemoveField(
            model_name='region',
            name='country',
        ),
        migrations.AlterField(
            model_name='viewed',
            name='last_viewed',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 2, 8, 36, 43, 543090), verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0433\u043e \u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u0430'),
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Region',
        ),
    ]
