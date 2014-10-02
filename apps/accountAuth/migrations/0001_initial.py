# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table(u'Profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mugshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('privacy', self.gf('django.db.models.fields.CharField')(default='closed', max_length=15)),
            ('language', self.gf('django.db.models.fields.CharField')(default='ru', max_length=5)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='user', unique=True, to=orm['authModel.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'account', ['Profile'])

        # Adding model 'Session_ID'
        db.create_table(u'Session_ID', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_session_id', null=True, to=orm['authModel.User'])),
            ('sessionid', self.gf('django.db.models.fields.CharField')(max_length=32, unique=True, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 16, 0, 0), auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 16, 0, 0), auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'account', ['Session_ID'])

        # Adding model 'HttpRequest_META'
        db.create_table(u'HttpRequest_META', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Session_ID'])),
            ('content_length', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('http_accept_encoding', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('http_accept_language', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('http_host', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('http_referer', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('http_user_agent', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('query_string', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('remote_addr', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('remote_host', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('remote_user', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('request_method', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('server_name', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('server_port', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'account', ['HttpRequest_META'])


    def backwards(self, orm):
        # Deleting model 'Profile'
        db.delete_table(u'Profile')

        # Deleting model 'Session_ID'
        db.delete_table(u'Session_ID')

        # Deleting model 'HttpRequest_META'
        db.delete_table(u'HttpRequest_META')


    models = {
        u'account.httprequest_meta': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'HttpRequest_META', 'db_table': "u'HttpRequest_META'"},
            'content_length': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'http_accept_encoding': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'http_accept_language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'http_host': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'http_referer': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'http_user_agent': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query_string': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'remote_addr': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'remote_host': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'remote_user': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'request_method': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'server_name': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'server_port': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Session_ID']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'account.profile': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'Profile', 'db_table': "u'Profile'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '5'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'closed'", 'max_length': '15'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user'", 'unique': 'True', 'to': u"orm['authModel.User']"})
        },
        u'account.session_id': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'Session_ID', 'db_table': "u'Session_ID'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 16, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sessionid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 16, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_session_id'", 'null': 'True', 'to': u"orm['authModel.User']"})
        },
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
        u'authModel.user': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'User', 'db_table': "u'UserModel'"},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'carrier': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "u'\\u0423\\u043a\\u0440\\u0430\\u0438\\u043d\\u0430'", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'email_delivery_new_products': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email_delivery_shares_news': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'patronymic': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '19', 'null': 'True', 'blank': 'True'}),
            'settlement': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['account']