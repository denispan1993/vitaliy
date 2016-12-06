# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.utils.captcha.utils


class Migration(migrations.Migration):

    dependencies = [
        ('authModel', '0007_email_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='hash',
            field=models.CharField(default=apps.utils.captcha.utils.key_generator, max_length=16, verbose_name='Hash'),
        ),
    ]
