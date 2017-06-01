# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery2', '0004_auto_20161128_0016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messageredirecturl',
            name='delivery',
        ),
        migrations.AddField(
            model_name='messageredirecturl',
            name='message',
            field=models.ForeignKey(verbose_name='\u041f\u0438\u0441\u044c\u043c\u043e', blank=True, to='delivery2.Message', null=True),
        ),
        migrations.AddField(
            model_name='messageredirecturl',
            name='type',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='\u0422\u0438\u043f URL', choices=[(1, 'Url'), (2, 'Unsub'), (3, 'Show online')]),
        ),
    ]
