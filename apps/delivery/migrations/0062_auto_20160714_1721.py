# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0061_rawemail_message_id_header'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mailaccount',
            old_name='is_active',
            new_name='use_smtp',
        ),
        migrations.AddField(
            model_name='mailaccount',
            name='use_imap',
            field=models.BooleanField(default=False, verbose_name='Use IMAP protocol'),
        ),
        migrations.AddField(
            model_name='mailaccount',
            name='use_pop3',
            field=models.BooleanField(default=False, verbose_name='Use POP3 protocol'),
        ),
    ]
