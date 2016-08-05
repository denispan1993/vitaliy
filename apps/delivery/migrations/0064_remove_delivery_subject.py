# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.apps import apps as global_apps


def forwards_func(apps, schema_editor):
    try:
        Delivery = apps.get_model('delivery', 'Delivery')
    except LookupError:
        return

    Subject = apps.get_model('delivery', 'Subject')
    Subject.objects.bulk_create([
        Subject(delivery=delivery, subject=delivery.subject, chance=1, )
        for delivery in Delivery.objects.all()]
    )


def reverse_func(apps, schema_editor):
    return None


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0063_auto_20160727_2229'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
