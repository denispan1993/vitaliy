# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product',
            field=models.ForeignKey(verbose_name='\u041f\u0440\u043e\u0434\u0443\u043a\u0442', to='product.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.ForeignKey(verbose_name='\u0421\u0442\u0440\u0430\u043d\u0430', blank=True, to='product.Country', null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_company',
            field=models.ForeignKey(verbose_name='\u041a\u043e\u043c\u043f\u0430\u043d\u0438\u044f \u0434\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a', blank=True, to='cart.DeliveryCompany', null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
