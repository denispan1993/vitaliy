# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_auto_20150913_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 18, 10, 11, 0, 297617), auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.CharField(default=b'2015-09-18T10:11:00.297495', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 18, 10, 11, 0, 297644), auto_now=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailfordelivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 18, 10, 11, 0, 331666), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailfordelivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 18, 10, 11, 0, 331695), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailmiddledelivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 18, 10, 11, 0, 298266), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailmiddledelivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 18, 10, 11, 0, 298290), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', blank=True),
            preserve_default=True,
        ),
    ]
