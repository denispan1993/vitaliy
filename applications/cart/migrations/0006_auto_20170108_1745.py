# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_auto_20170107_2248'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='custom_price',
            new_name='is_custom_price',
        ),
    ]
