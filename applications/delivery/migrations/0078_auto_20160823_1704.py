# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0077_auto_20160823_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='type',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='\u0422\u0438\u043f URL', choices=[(1, 'Url'), (2, 'Unsub'), (3, 'Open')]),
        ),
        migrations.AlterField(
            model_name='url',
            name='anchor',
            field=models.CharField(max_length=256, null=True, verbose_name='\u042f\u043a\u043e\u0440\u044c --> "\u0410\u043d\u043a\u043e\u0440"', blank=True),
        ),
        migrations.AlterField(
            model_name='url',
            name='title',
            field=models.CharField(max_length=256, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AlterField(
            model_name='url',
            name='url_id',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Url ID', blank=True),
        ),
    ]
