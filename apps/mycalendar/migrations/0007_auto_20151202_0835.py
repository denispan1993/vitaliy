# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycalendar', '0006_auto_20151201_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='leading_course',
        ),
        migrations.RemoveField(
            model_name='event',
            name='location_date_time',
        ),
        migrations.RemoveField(
            model_name='event',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='event',
            name='user',
        ),
        migrations.RemoveField(
            model_name='locationdatetime',
            name='city',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='LeadingCourse',
        ),
        migrations.DeleteModel(
            name='LocationDateTime',
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
    ]
