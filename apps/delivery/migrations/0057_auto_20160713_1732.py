# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0056_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailaccount',
            options={'ordering': ['-created_at'], 'get_latest_by': 'pk', 'verbose_name': 'Mail Account', 'verbose_name_plural': 'Mail Accounts'},
        ),
    ]
