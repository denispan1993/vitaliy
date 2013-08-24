# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Static'
        db.create_table('Static_Pages', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, unique=True, null=True, blank=True)),
            ('url', self.gf('compat.FormSlug.models.ModelSlugField')(max_length=50, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('meta_title', self.gf('django.db.models.fields.CharField')(max_length=190, null=True, blank=True)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=190, null=True, blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(max_length=160, null=True, blank=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('visibility', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'static', ['Static'])


    def backwards(self, orm):
        # Deleting model 'Static'
        db.delete_table('Static_Pages')


    models = {
        u'static.static': {
            'Meta': {'ordering': "['order']", 'object_name': 'Static', 'db_table': "'Static_Pages'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '190', 'null': 'True', 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'max_length': '190', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'url': ('compat.FormSlug.models.ModelSlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'visibility': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['static']