# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0008_auto_20150921_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='send_general',
            field=models.BooleanField(default=True, verbose_name='\u0413\u043b\u0430\u0432\u043d\u0430\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0430 \u043e\u0442\u043e\u0441\u043b\u0430\u043d\u0430'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='delivery',
            name='send_test',
            field=models.BooleanField(default=True, verbose_name='\u0422\u0435\u0441\u0442\u043e\u0432\u0430\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0430 \u043e\u0442\u043e\u0441\u043b\u0430\u043d\u0430'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 15, 48, 5, 50236), auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.CharField(default=b'2015-09-22T15:48:05.050033', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 15, 48, 5, 50265), auto_now=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailfordelivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 15, 48, 5, 57253), auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailfordelivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 15, 48, 5, 57285), auto_now=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailmiddledelivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 15, 48, 5, 51056), auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailmiddledelivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 15, 48, 5, 51083), auto_now=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f'),
            preserve_default=True,
        ),
    ]
