# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authModel', '0004_email_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email',
            old_name='email_delivery_new_products',
            new_name='delivery_new_products',
        ),
        migrations.RenameField(
            model_name='email',
            old_name='email_delivery_shares_news',
            new_name='delivery_shares_news',
        ),
        migrations.AddField(
            model_name='email',
            name='delivery_spam',
            field=models.BooleanField(default=True, verbose_name='\u0421\u043f\u0430\u043c'),
        ),
    ]
