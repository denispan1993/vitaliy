# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0067_remove_url_url_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='url_id',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Url ID'),
        ),
    ]
