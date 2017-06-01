# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_auto_20150913_1300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailfordelivery',
            options={'ordering': ['-created_at'], 'verbose_name': '\u041c\u043e\u0434\u0435\u043b\u044c \u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0438 (Email \u0430\u0434\u0440\u0435\u0441)', 'verbose_name_plural': '\u041c\u043e\u0434\u0435\u043b\u0438 \u0420\u0430\u0441\u0441\u044b\u043b\u043e\u043a (Email \u0430\u0434\u0440\u0435\u0441\u0430)'},
        ),
        migrations.AlterModelOptions(
            name='emailmiddledelivery',
            options={'ordering': ['-created_at'], 'verbose_name': '\u041f\u0440\u043e\u043c\u0435\u0436\u0443\u0442\u043e\u0447\u043d\u0430\u044f \u043c\u043e\u0436\u0435\u043b\u044c \u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0438', 'verbose_name_plural': '\u041f\u0440\u043e\u043c\u0435\u0436\u0443\u0442\u043e\u0447\u043d\u044b\u0435 \u043c\u043e\u0436\u0435\u043b\u0438 \u0420\u0430\u0441\u0441\u044b\u043b\u043e\u043a'},
        ),
        migrations.AlterField(
            model_name='delivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 13, 9, 34, 911671), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.CharField(default=b'2015-09-13T13:09:34.911419', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 13, 9, 34, 911718), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailfordelivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 13, 9, 34, 923326), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailfordelivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 13, 9, 34, 923380), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailmiddledelivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 13, 9, 34, 912954), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailmiddledelivery',
            name='delivery',
            field=models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0443', to='delivery.Delivery'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailmiddledelivery',
            name='delivery_test',
            field=models.BooleanField(default=True, verbose_name='\u0422\u0435\u0441\u0442\u043e\u0432\u0430\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0430 - \u043e\u0442\u043e\u0441\u043b\u0430\u043d\u0430'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailmiddledelivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 13, 13, 9, 34, 913001), null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', blank=True),
            preserve_default=True,
        ),
    ]
