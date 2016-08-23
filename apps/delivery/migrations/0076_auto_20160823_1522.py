# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('delivery', '0075_auto_20160818_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='traceofvisits',
            name='content_type',
            field=models.ForeignKey(verbose_name='\u0423\u043a\u0430\u0437\u0430\u0442\u0435\u043b\u044c \u043d\u0430 E-Mail', blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='traceofvisits',
            name='object_id',
            field=models.PositiveIntegerField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='traceofvisits',
            name='target_id',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='\u0422\u0438\u043f \u0446\u044d\u043b\u0438 \u043e\u0431\u0440\u0430\u0449\u0435\u043d\u0438\u044f \u043a \u0441\u0430\u0439\u0442\u0443', blank=True),
        ),
    ]
