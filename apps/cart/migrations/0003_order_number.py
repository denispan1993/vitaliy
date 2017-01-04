# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20151113_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='number',
            field=models.PositiveIntegerField(default=1, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0437\u0430\u043a\u0430\u0437\u0430'),
            preserve_default=False,
        ),
    ]
