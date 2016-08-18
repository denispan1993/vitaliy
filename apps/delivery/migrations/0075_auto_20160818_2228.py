# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0074_auto_20160818_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 subject', blank=True, to='delivery.Subject', null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='subject_str',
            field=models.CharField(max_length=256, null=True, verbose_name='\u0421\u0442\u0440\u043e\u043a\u0430 subject', blank=True),
        ),
    ]
