# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery2', '0007_auto_20170110_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailtemplate',
            name='is_system',
        ),
    ]
