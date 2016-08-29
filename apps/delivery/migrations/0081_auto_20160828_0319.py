# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0080_proxyserver'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proxyserver',
            old_name='sock4',
            new_name='socks4',
        ),
        migrations.RenameField(
            model_name='proxyserver',
            old_name='sock5',
            new_name='socks5',
        ),
    ]
