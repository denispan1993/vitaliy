# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycalendar', '0010_auto_20160517_2125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='title',
        ),
        migrations.AlterField(
            model_name='event',
            name='topic',
            field=models.CharField(default=b'', max_length=256, verbose_name='\u0422\u0435\u043c\u0430 \u043a\u0443\u0440\u0441\u0430'),
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
    ]
