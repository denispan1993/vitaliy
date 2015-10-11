# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.delivery.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0017_auto_20151011_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailfordelivery',
            name='key',
            field=models.CharField(default=apps.delivery.models.key_generate_for_email_delivery, unique=True, max_length=8, verbose_name='ID E-Mail \u0430\u0434\u0440\u0435\u0441\u0430 \u0438 \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 19, 27, 59, 480610), auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.CharField(default=b'2015-10-11T19:27:59.480213', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 19, 27, 59, 480665), auto_now=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailfordelivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 19, 27, 59, 495523), auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailfordelivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 19, 27, 59, 495589), auto_now=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailmiddledelivery',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 19, 27, 59, 482526), auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='emailmiddledelivery',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 19, 27, 59, 482593), auto_now=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mailaccount',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 19, 27, 59, 478869), auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mailaccount',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 19, 27, 59, 478936), auto_now=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='traceofvisits',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 19, 27, 59, 497005), auto_now_add=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
            preserve_default=True,
        ),
    ]
