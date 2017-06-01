# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import applications.delivery.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0052_auto_20160507_2145'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mailserver',
            old_name='server',
            new_name='server_smtp',
        ),
        migrations.RenameField(
            model_name='mailserver',
            old_name='port',
            new_name='port_smtp',
        ),
        migrations.RenameField(
            model_name='mailserver',
            old_name='use_ssl',
            new_name='use_ssl_smtp',
        ),
        migrations.RenameField(
            model_name='mailserver',
            old_name='use_tls',
            new_name='use_tls_smtp',
        ),
        migrations.AddField(
            model_name='mailserver',
            name='port_imap',
            field=models.PositiveSmallIntegerField(default=25, null=True, verbose_name='IMAP Port', blank=True),
        ),
        migrations.AddField(
            model_name='mailserver',
            name='port_pop3',
            field=models.PositiveSmallIntegerField(default=110, null=True, verbose_name='POP3 Port', blank=True),
        ),
        migrations.AddField(
            model_name='mailserver',
            name='server_imap',
            field=models.CharField(max_length=128, null=True, verbose_name='IMAP Server', blank=True),
        ),
        migrations.AddField(
            model_name='mailserver',
            name='server_name',
            field=models.CharField(max_length=64, null=True, verbose_name='Server Name', blank=True),
        ),
        migrations.AddField(
            model_name='mailserver',
            name='server_pop3',
            field=models.CharField(max_length=128, null=True, verbose_name='POP3 Server', blank=True),
        ),
        migrations.AddField(
            model_name='mailserver',
            name='use_imap',
            field=models.BooleanField(default=False, verbose_name='Use IMAP protocol'),
        ),
        migrations.AddField(
            model_name='mailserver',
            name='use_pop3',
            field=models.BooleanField(default=False, verbose_name='Use POP3 protocol'),
        ),
        migrations.AddField(
            model_name='mailserver',
            name='use_ssl_imap',
            field=models.BooleanField(default=False, verbose_name='IMAP Use SSL'),
        ),
        migrations.AddField(
            model_name='mailserver',
            name='use_ssl_pop3',
            field=models.BooleanField(default=False, verbose_name='POP3 Use SSL'),
        ),
        migrations.AddField(
            model_name='mailserver',
            name='use_tls_imap',
            field=models.BooleanField(default=True, verbose_name='IMAP Use TLS'),
        ),
        migrations.AddField(
            model_name='mailserver',
            name='use_tls_pop3',
            field=models.BooleanField(default=True, verbose_name='POP3 Use TLS'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.CharField(default=applications.delivery.models.datetime_in_iso_format, max_length=128, null=True, verbose_name='\u0418\u043c\u044f \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='mailaccount',
            name='auto_active_datetime',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='\u0414\u0430\u0442\u0430 \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044f \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430'),
        ),
        migrations.AlterField(
            model_name='mailaccount',
            name='server',
            field=models.ForeignKey(verbose_name='Server', to='delivery.MailServer'),
        ),
    ]
