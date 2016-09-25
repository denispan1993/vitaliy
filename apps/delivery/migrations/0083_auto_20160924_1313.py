# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0082_auto_20160828_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proxyserver',
            name='from_whence',
            field=models.PositiveSmallIntegerField(verbose_name='\u041e\u0442\u043a\u0443\u0434\u0430', choices=[(1, 'http://hideme.ru'), (2, 'http://socks-proxy.net'), (3, 'http://gatherproxy.com')]),
        ),
    ]
