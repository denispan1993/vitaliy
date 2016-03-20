# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_auto_20151204_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='title',
            field=models.TextField(null=True, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u044f', blank=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='type',
            field=models.PositiveSmallIntegerField(blank=True, null=True, choices=[(0, b'comment'), (1, b'opinion')]),
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(default=None, help_text='\u041a\u0430\u043a \u0447\u0435\u043b\u043e\u0432\u0435\u043a \u043f\u0440\u0435\u0434\u0441\u0442\u0430\u0432\u0438\u043b\u0441\u044f, \u0438\u043c\u044f \u043a\u043e\u0442\u043e\u0440\u043e\u0435 \u0431\u0443\u0434\u0435\u0442 \u0432\u044b\u0432\u043e\u0434\u0438\u0442\u0441\u044f \u043d\u0430 \u0441\u0430\u0439\u0442\u0435.', max_length=64, verbose_name='\u0418\u043c\u044f \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0442\u043e\u0440\u0430'),
        ),
    ]
