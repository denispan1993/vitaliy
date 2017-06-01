# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authModel', '0008_email_hash'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='phone',
            options={'ordering': ['-created_at'], 'verbose_name': '\u0422\u0435\u043b\u0435\u0444\u043e\u043d \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f', 'verbose_name_plural': '\u0422\u0435\u043b\u0435\u0444\u043e\u043d\u044b \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439'},
        ),
        migrations.AddField(
            model_name='phone',
            name='int_code',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='\u041a\u043e\u0434  \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430', blank=True),
        ),
        migrations.AddField(
            model_name='phone',
            name='int_phone',
            field=models.PositiveIntegerField(null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430', blank=True),
        ),
    ]
