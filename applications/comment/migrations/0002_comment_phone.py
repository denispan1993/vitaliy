# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='phone',
            field=models.CharField(default=None, max_length=32, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f', blank=True),
        ),
    ]
