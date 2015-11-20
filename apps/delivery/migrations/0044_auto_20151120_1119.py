# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0043_auto_20151114_2142'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email_img',
            old_name='img',
            new_name='image',
        ),
#        migrations.AddField(
#            model_name='mailaccount',
#            name='is_auto_active',
#            field=models.BooleanField(default=True, verbose_name='\u0410\u043a\u043a\u0430\u0443\u043d\u0442 \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438 \u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0439'),
#        ),
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.CharField(default=b'2015-11-20T11:19:37.705588', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='mailaccount',
            name='auto_active_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 20, 11, 19, 37, 697193), verbose_name='\u0414\u0430\u0442\u0430 \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044f \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430'),
        ),
    ]
