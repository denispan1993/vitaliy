# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0044_auto_20151120_1119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email_img',
            name='content_type',
        ),
        migrations.AlterModelOptions(
            name='emailfordelivery',
            options={'ordering': ['-created_at'], 'verbose_name': '\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0430 (Email \u0430\u0434\u0440\u0435\u0441)', 'verbose_name_plural': '\u0420\u0430\u0441\u0441\u044b\u043b\u043a\u0438 (Email \u0430\u0434\u0440\u0435\u0441\u0430)'},
        ),
        migrations.AlterModelOptions(
            name='traceofvisits',
            options={'ordering': ['-created_at'], 'verbose_name': '\u0421\u043b\u0435\u0434 \u043e\u0442 \u043f\u043e\u0441\u0435\u0449\u0435\u043d\u0438\u044f', 'verbose_name_plural': '\u0421\u043b\u0435\u0434\u044b \u043e\u0442 \u043f\u043e\u0441\u0435\u0449\u0435\u043d\u0438\u0439'},
        ),
#        migrations.AddField(
#            model_name='mailaccount',
#            name='is_auto_active',
#            field=models.BooleanField(default=True, verbose_name='\u0410\u043a\u043a\u0430\u0443\u043d\u0442 \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438 \u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0439'),
#        ),
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.CharField(default=b'2015-11-20T13:01:04.224714', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='mailaccount',
            name='auto_active_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 20, 13, 1, 4, 219804), verbose_name='\u0414\u0430\u0442\u0430 \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044f \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430'),
        ),
        migrations.DeleteModel(
            name='Email_Img',
        ),
    ]
