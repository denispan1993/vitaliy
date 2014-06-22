# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Captcha_Key.next_use'
        db.add_column('Captcha_Keys', 'next_use',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 22, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Captcha_Key.next_use'
        db.delete_column('Captcha_Keys', 'next_use')


    models = {
        u'captcha.captcha_images': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Captcha_Images', 'db_table': "'Captcha_Images'"},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'image_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'captcha.captcha_key': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Captcha_Key', 'db_table': "'Captcha_Keys'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['captcha.Captcha_Images']"}),
            'image_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'OXZTaxgG'", 'max_length': '8'}),
            'next_use': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 22, 0, 0)'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['captcha']