# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import compat.FormSlug.models


class Migration(migrations.Migration):

    dependencies = [
        ('mycalendar', '0008_auto_20151202_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadingcourse',
            name='url',
            field=compat.FormSlug.models.ModelSlugField(db_index=True, max_length=255, null=True, verbose_name='URL \u0430\u0434\u0440\u0435\u0441 \u0412\u0435\u0434\u0443\u0449\u0435\u0433\u043e', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location_date_time',
            field=models.ManyToManyField(to='mycalendar.LocationDateTime', verbose_name='\u041c\u0435\u0441\u0442\u043e \u0434\u0430\u0442\u0430 \u0438 \u0432\u0440\u0435\u043c\u044f \u043f\u0440\u043e\u0432\u0435\u0434\u0435\u043d\u0438\u044f'),
        ),
    ]
