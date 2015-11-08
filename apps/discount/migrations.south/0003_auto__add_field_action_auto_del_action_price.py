# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Action.auto_del_action_price'
        db.add_column(u'Action', 'auto_del_action_price',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Action.auto_del_action_price'
        db.delete_column(u'Action', 'auto_del_action_price')


    models = {
        u'discount.action': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'Action', 'db_table': "u'Action'"},
            'auto_del': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_del_action_price': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_end': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'auto_start': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datetime_end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 23, 0, 0)'}),
            'datetime_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 16, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u'\\u0410\\u043a\\u0446\\u0438\\u044f'", 'max_length': '256'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['discount']