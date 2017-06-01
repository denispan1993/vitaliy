# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0084_delete_proxyserver'),
    ]

    operations = [
        migrations.AddField(
            model_name='spamemail',
            name='test',
            field=models.BooleanField(default=False, verbose_name="\u0422\u0435\u0441\u0442 e'mail"),
        ),
    ]
