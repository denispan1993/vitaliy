# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0070_auto_20160804_1655'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='html',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='real_html',
        ),
    ]
