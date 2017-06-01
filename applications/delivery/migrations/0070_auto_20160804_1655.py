# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.apps import apps as global_apps


def forwards_func(apps, schema_editor):
    try:
        Delivery = apps.get_model('delivery', 'Delivery')
    except LookupError:
        return

    Html = apps.get_model('delivery', 'Body')
    Html.objects.bulk_create([
        Html(delivery=delivery,
             html=delivery.html,
             real_html=delivery.real_html if delivery.real_html else '',
             chance=1, )
        for delivery in Delivery.objects.all()]
    )


def reverse_func(apps, schema_editor):
    return None


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0069_auto_20160804_1653'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]

