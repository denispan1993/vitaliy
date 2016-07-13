# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0059_rawemail'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawemail',
            name='subject_header',
            field=models.TextField(null=True, verbose_name='Subject header', blank=True),
        ),
    ]
