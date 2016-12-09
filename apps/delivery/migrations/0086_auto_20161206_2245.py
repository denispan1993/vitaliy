# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.delivery.models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0085_spamemail_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='spamemail',
            name='hash',
            field=models.CharField(default=apps.delivery.models.hash_16, max_length=16, verbose_name='Hash'),
        ),
        migrations.AlterField(
            model_name='emailfordelivery',
            name='key',
            field=models.CharField(default=apps.delivery.models.hash_8, max_length=8, verbose_name='ID E-Mail \u0430\u0434\u0440\u0435\u0441\u0430 \u0438 \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438'),
        ),
        migrations.AlterField(
            model_name='messageurl',
            name='key',
            field=models.CharField(default=apps.delivery.models.hash_64, max_length=64, verbose_name='ID E-Mail \u0430\u0434\u0440\u0435\u0441\u0430 \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438 \u0438 Url'),
        ),
    ]
