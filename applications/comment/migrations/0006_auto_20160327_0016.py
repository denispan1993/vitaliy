# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0005_auto_20160320_1516'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='email_for_response',
            new_name='email',
        ),
    ]
