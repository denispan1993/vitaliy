# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Setting.variable_positivesmallinteger'
        db.delete_column('Setting', 'variable_positivesmallinteger')

        # Deleting field 'Setting.variable_char'
        db.delete_column('Setting', 'variable_char')

        # Adding field 'Setting.char'
        db.add_column('Setting', 'char',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Setting.text'
        db.add_column('Setting', 'text',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Setting.integer'
        db.add_column('Setting', 'integer',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Setting.positivesmallinteger'
        db.add_column('Setting', 'positivesmallinteger',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Setting.variable_positivesmallinteger'
        db.add_column('Setting', 'variable_positivesmallinteger',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Setting.variable_char'
        db.add_column('Setting', 'variable_char',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Setting.char'
        db.delete_column('Setting', 'char')

        # Deleting field 'Setting.text'
        db.delete_column('Setting', 'text')

        # Deleting field 'Setting.integer'
        db.delete_column('Setting', 'integer')

        # Deleting field 'Setting.positivesmallinteger'
        db.delete_column('Setting', 'positivesmallinteger')


    models = {
        u'setting.setting': {
            'Meta': {'ordering': "['created_at']", 'object_name': 'Setting', 'db_table': "'Setting'"},
            'char': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'integer': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'positivesmallinteger': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'variable_name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '128'})
        }
    }

    complete_apps = ['setting']