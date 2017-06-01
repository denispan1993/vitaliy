# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_category_id_1c'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='id_1c',
            field=models.CharField(max_length=36, null=True, verbose_name='1C \u0418\u0434', blank=True),
        ),
    ]
