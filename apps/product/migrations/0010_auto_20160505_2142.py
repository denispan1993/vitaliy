# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20160102_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_availability',
            field=models.IntegerField(default=1, verbose_name='\u041d\u0430\u043b\u0438\u0447\u0438\u0435', choices=[(1, '\u0415\u0441\u0442\u044c \u0432 \u043d\u0430\u043b\u0438\u0447\u0438\u0438'), (2, '\u041f\u043e\u0434 \u0437\u0430\u043a\u0430\u0437'), (3, '\u041e\u0436\u0438\u0434\u0430\u0435\u0442\u0441\u044f'), (4, '\u041d\u0435\u0434\u043e\u0441\u0442\u0443\u043f\u0435\u043d')]),
        ),
        migrations.AlterField(
            model_name='viewed',
            name='last_viewed',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 5, 21, 42, 4, 246853), verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0433\u043e \u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u0430'),
        ),
    ]
