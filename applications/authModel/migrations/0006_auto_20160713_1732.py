# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authModel', '0005_auto_20151216_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='error550',
            field=models.BooleanField(default=False, verbose_name='Error 550'),
        ),
        migrations.AddField(
            model_name='email',
            name='error550_date',
            field=models.DateField(null=True, verbose_name='Error 550 Date', blank=True),
        ),
    ]
