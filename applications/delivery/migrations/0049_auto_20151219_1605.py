# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0048_auto_20151219_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='traceofvisits',
            name='target',
            field=models.CharField(max_length=32, null=True, verbose_name='\u0426\u044d\u043b\u044c \u0437\u0430\u0445\u043e\u0434\u0430 \u043d\u0430 \u0441\u0430\u0439\u0442', blank=True),
        ),
        migrations.AddField(
            model_name='traceofvisits',
            name='target_id',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='\u0422\u0438\u043f \u0446\u044d\u043b\u0438 \u0437\u0430\u0445\u043e\u0434\u0430 \u043d\u0430 \u0441\u0430\u0439\u0442', blank=True),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.CharField(default=b'2015-12-19T16:05:42.542288', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='mailaccount',
            name='auto_active_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 19, 16, 5, 42, 538175), verbose_name='\u0414\u0430\u0442\u0430 \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044f \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430'),
        ),
    ]
