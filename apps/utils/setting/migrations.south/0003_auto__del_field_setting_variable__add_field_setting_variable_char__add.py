# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Setting.variable'
        db.delete_column('Setting', 'variable')

        # Adding field 'Setting.variable_char'
        db.add_column('Setting', 'variable_char',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Setting.variable_positivesmallinteger'
        db.add_column('Setting', 'variable_positivesmallinteger',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Setting.variable'
        db.add_column('Setting', 'variable',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Setting.variable_char'
        db.delete_column('Setting', 'variable_char')

        # Deleting field 'Setting.variable_positivesmallinteger'
        db.delete_column('Setting', 'variable_positivesmallinteger')


    models = {
        u'setting.setting': {
            'Meta': {'ordering': "['created_at']", 'object_name': 'Setting', 'db_table': "'Setting'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'variable_char': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'variable_name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '128'}),
            'variable_positivesmallinteger': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['setting']