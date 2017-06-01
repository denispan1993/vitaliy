# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0046_auto_20151120_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='spamemail',
            name='delivery_new_products',
            field=models.BooleanField(default=True, verbose_name='\u041d\u043e\u0432\u044b\u0435 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u044b'),
        ),
        migrations.AddField(
            model_name='spamemail',
            name='delivery_shares_news',
            field=models.BooleanField(default=True, verbose_name='\u041d\u043e\u0432\u043e\u0441\u0442\u0438 \u0438 \u0410\u043a\u0446\u0438\u0438'),
        ),
        migrations.AddField(
            model_name='spamemail',
            name='delivery_spam',
            field=models.BooleanField(default=True, verbose_name='\u0421\u043f\u0430\u043c'),
        ),
        migrations.AddField(
            model_name='spamemail',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 16, 7, 49, 4, 746556, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.CharField(default=b'2015-12-16T09:48:53.135032', max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='mailaccount',
            name='auto_active_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 16, 9, 48, 53, 131784), verbose_name='\u0414\u0430\u0442\u0430 \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044f \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430'),
        ),
    ]
