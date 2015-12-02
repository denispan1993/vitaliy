# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20151202_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewed',
            name='last_viewed',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 2, 8, 47, 22, 789895), verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0433\u043e \u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u0430'),
        ),
    ]
