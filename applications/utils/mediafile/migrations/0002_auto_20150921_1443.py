# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mediafile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediafile',
            name='height',
            field=models.PositiveIntegerField(default=1, null=True, verbose_name='\u0412\u044b\u0441\u043e\u0442\u0430 \u0444\u0430\u0439\u043b\u0430', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mediafile',
            name='number',
            field=models.PositiveIntegerField(default=1, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0444\u0430\u0439\u043b\u0430 \u0432 \u0442\u0435\u043a\u0441\u0442\u0435'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mediafile',
            name='width',
            field=models.PositiveIntegerField(default=1, null=True, verbose_name='\u0428\u0438\u0440\u0438\u043d\u0430 \u0444\u0430\u0439\u043b\u0430', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mediafile',
            name='title',
            field=models.CharField(help_text='title \\<a> \u0437\u0430\u043f\u0438\u0441\u0438.', max_length=256, null=True, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a', blank=True),
            preserve_default=True,
        ),
    ]
