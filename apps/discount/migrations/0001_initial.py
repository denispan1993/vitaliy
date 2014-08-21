# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Action'
        db.create_table(u'Action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime_start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 16, 0, 0))),
            ('datetime_end', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 23, 0, 0))),
            ('auto_start', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('auto_end', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('auto_del', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'discount', ['Action'])


    def backwards(self, orm):
        # Deleting model 'Action'
        db.delete_table(u'Action')


    models = {
        u'discount.action': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'Action', 'db_table': "u'Action'"},
            'auto_del': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_end': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'auto_start': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datetime_end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 23, 0, 0)'}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 16, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['discount']