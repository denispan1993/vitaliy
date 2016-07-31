# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0066_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='url',
            name='url_id',
        ),
    ]
