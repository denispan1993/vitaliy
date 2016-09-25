# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0083_auto_20160924_1313'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProxyServer',
        ),
    ]
