# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0064_remove_delivery_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='subject',
        ),
    ]
