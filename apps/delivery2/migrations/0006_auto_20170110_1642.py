# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery2', '0005_auto_20161202_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtemplate',
            name='is_system',
            field=models.BooleanField(default=False, verbose_name='\u0421\u0438\u0441\u0442\u0435\u043c\u043d\u044b\u0439'),
        ),
        migrations.AlterField(
            model_name='messageredirecturl',
            name='type',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='\u0422\u0438\u043f URL', choices=[(1, 'Url'), (2, 'Unsub'), (3, 'Open'), (4, 'Show online')]),
        ),
    ]
