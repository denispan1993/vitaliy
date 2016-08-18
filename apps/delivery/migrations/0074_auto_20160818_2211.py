# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0073_auto_20160818_2205'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='body',
            table='Delivery_Body',
        ),
    ]
