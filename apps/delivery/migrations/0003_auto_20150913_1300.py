# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_auto_20150913_1258'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailmiddledelivery',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='delivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 13, 0, 0, 763794), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.CharField(default=b'2015-09-13T13:00:00.763540', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 13, 0, 0, 763842), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailfordelivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 13, 0, 0, 775328), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailfordelivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 13, 0, 0, 775381), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailmiddledelivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 13, 0, 0, 765050), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailmiddledelivery',
            name='delivery',
            field=models.ForeignKey(to='delivery.Delivery'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailmiddledelivery',
            name='delivery_test',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailmiddledelivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 13, 0, 0, 765096), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', blank=True),
            preserve_default=True,
        ),
    ]
