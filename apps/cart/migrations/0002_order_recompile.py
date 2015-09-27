# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='recompile',
            field=models.BooleanField(default=False, verbose_name='\u0420\u0430\u0437\u0431\u043e\u0440 \u0417\u0430\u043a\u0430\u0437\u0430'),
            preserve_default=True,
        ),
    ]
