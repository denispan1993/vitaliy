# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Setting.variable_name'
        db.alter_column('Setting', 'variable_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128))

        # Changing field 'Setting.name'
        db.alter_column('Setting', 'name', self.gf('django.db.models.fields.CharField')(max_length=128))

    def backwards(self, orm):

        # Changing field 'Setting.variable_name'
        db.alter_column('Setting', 'variable_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, null=True))

        # Changing field 'Setting.name'
        db.alter_column('Setting', 'name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True))

    models = {
        u'setting.setting': {
            'Meta': {'ordering': "['created_at']", 'object_name': 'Setting', 'db_table': "'Setting'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'variable': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'variable_name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '128'})
        }
    }

    complete_apps = ['setting']