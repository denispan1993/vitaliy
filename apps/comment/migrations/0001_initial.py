# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Comment'
        db.create_table('Comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment_parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name=u'children', null=True, to=orm['comment.Comment'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_Product', to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('serial_number', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('shown_colored', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('shown_bold', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('shown_italic', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('font_px', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=14)),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, max_length=64)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('sessionid', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('rating', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('pass_moderation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('require_a_response', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email_for_response', self.gf('django.db.models.fields.CharField')(default=None, max_length=64, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('mptt_level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'comment', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Comment'
        db.delete_table('Comment')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
#        u'auth.1user': {
#            'Meta': {'object_name': 'User'},
#            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
#            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
#            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
#            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
#            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
#            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
#            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
#            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
#            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
#            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
#            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
#            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
#            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
#        },
        u'comment.comment': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Comment', 'db_table': "'Comment'"},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'comment_parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': u"orm['comment.Comment']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_Product'", 'to': u"orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_for_response': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'font_px': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '14'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'pass_moderation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rating': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'require_a_response': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'serial_number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'sessionid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'shown_bold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shown_colored': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shown_italic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['comment']