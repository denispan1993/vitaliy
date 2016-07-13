# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0057_auto_20160713_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='spamemail',
            name='error550',
            field=models.BooleanField(default=False, verbose_name='Error 550'),
        ),
        migrations.AddField(
            model_name='spamemail',
            name='error550_date',
            field=models.DateField(null=True, verbose_name='Error 550 Date', blank=True),
        ),
    ]
