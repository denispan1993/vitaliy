# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authModel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='bad_email',
            field=models.BooleanField(default=False, verbose_name='Bad E-Mail'),
            preserve_default=True,
        ),
    ]
