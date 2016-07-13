# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0060_rawemail_subject_header'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawemail',
            name='message_id_header',
            field=models.CharField(max_length=255, null=True, verbose_name='Message-Id header', blank=True),
        ),
    ]
