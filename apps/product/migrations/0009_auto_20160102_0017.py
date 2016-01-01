# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20151202_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='currency_code_char',
            field=models.CharField(default=b'UAH', max_length=3, verbose_name='\u041a\u043e\u0434 \u0432\u0430\u043b\u044e\u0442\u044b \u0431\u0443\u043a\u0432\u0435\u043d\u043d\u044b\u0439'),
        ),
        migrations.AddField(
            model_name='currency',
            name='currency_code_number',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='\u041a\u043e\u0434 \u0432\u0430\u043b\u044e\u0442\u044b \u0447\u0438\u0441\u043b\u043e\u0432\u043e\u0439'),
        ),
        migrations.AlterField(
            model_name='viewed',
            name='last_viewed',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 2, 0, 17, 20, 227114), verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0433\u043e \u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u0430'),
        ),
    ]
