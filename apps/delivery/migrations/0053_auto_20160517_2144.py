# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.delivery.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0052_auto_20160507_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.CharField(default=apps.delivery.models.datetime_in_iso_format, max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='mailaccount',
            name='auto_active_datetime',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430 \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044f \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430'),
        ),
    ]
