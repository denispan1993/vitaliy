# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0072_auto_20160818_2159'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='body',
            table='Temp_Body',
        ),
    ]
