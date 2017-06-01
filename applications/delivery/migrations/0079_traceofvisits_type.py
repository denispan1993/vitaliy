# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0078_auto_20160823_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='traceofvisits',
            name='type',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='\u0422\u0438\u043f URL', choices=[(1, 'Url'), (2, 'Unsub'), (3, 'Open')]),
        ),
    ]
