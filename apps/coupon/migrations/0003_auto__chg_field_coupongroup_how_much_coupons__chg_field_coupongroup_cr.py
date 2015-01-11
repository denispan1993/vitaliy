# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CouponGroup.how_much_coupons'
        db.alter_column('CouponGroup', 'how_much_coupons', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True))

        # Changing field 'CouponGroup.created_at'
        db.alter_column('CouponGroup', 'created_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'CouponGroup.number_of_possible_uses'
        db.alter_column('CouponGroup', 'number_of_possible_uses', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True))

        # Changing field 'CouponGroup.updated_at'
        db.alter_column('CouponGroup', 'updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'CouponGroup.percentage_discount'
        db.alter_column('CouponGroup', 'percentage_discount', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True))

        # Changing field 'CouponGroup.end_of_the_coupon'
        db.alter_column('CouponGroup', 'end_of_the_coupon', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'CouponGroup.start_of_the_coupon'
        db.alter_column('CouponGroup', 'start_of_the_coupon', self.gf('django.db.models.fields.DateTimeField')(null=True))
        # Removing M2M table for field child on 'Coupon'
        db.delete_table(db.shorten_name('Coupon_child'))

        # Adding M2M table for field child_cart on 'Coupon'
        m2m_table_name = db.shorten_name('Coupon_child_cart')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('coupon', models.ForeignKey(orm[u'coupon.coupon'], null=False)),
            ('cart', models.ForeignKey(orm[u'cart.cart'], null=False))
        ))
        db.create_unique(m2m_table_name, ['coupon_id', 'cart_id'])

        # Adding M2M table for field child_order on 'Coupon'
        m2m_table_name = db.shorten_name('Coupon_child_order')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('coupon', models.ForeignKey(orm[u'coupon.coupon'], null=False)),
            ('order', models.ForeignKey(orm[u'cart.order'], null=False))
        ))
        db.create_unique(m2m_table_name, ['coupon_id', 'order_id'])


        # Changing field 'Coupon.created_at'
        db.alter_column('Coupon', 'created_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Coupon.updated_at'
        db.alter_column('Coupon', 'updated_at', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):

        # Changing field 'CouponGroup.how_much_coupons'
        db.alter_column('CouponGroup', 'how_much_coupons', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

        # User chose to not deal with backwards NULL issues for 'CouponGroup.created_at'
        raise RuntimeError("Cannot reverse this migration. 'CouponGroup.created_at' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'CouponGroup.created_at'
        db.alter_column('CouponGroup', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'CouponGroup.number_of_possible_uses'
        db.alter_column('CouponGroup', 'number_of_possible_uses', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

        # User chose to not deal with backwards NULL issues for 'CouponGroup.updated_at'
        raise RuntimeError("Cannot reverse this migration. 'CouponGroup.updated_at' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'CouponGroup.updated_at'
        db.alter_column('CouponGroup', 'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'CouponGroup.percentage_discount'
        db.alter_column('CouponGroup', 'percentage_discount', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

        # Changing field 'CouponGroup.end_of_the_coupon'
        db.alter_column('CouponGroup', 'end_of_the_coupon', self.gf('django.db.models.fields.DateTimeField')())

        # User chose to not deal with backwards NULL issues for 'CouponGroup.start_of_the_coupon'
        raise RuntimeError("Cannot reverse this migration. 'CouponGroup.start_of_the_coupon' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'CouponGroup.start_of_the_coupon'
        db.alter_column('CouponGroup', 'start_of_the_coupon', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))
        # Adding M2M table for field child on 'Coupon'
        m2m_table_name = db.shorten_name('Coupon_child')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('coupon', models.ForeignKey(orm[u'coupon.coupon'], null=False)),
            ('order', models.ForeignKey(orm[u'cart.order'], null=False))
        ))
        db.create_unique(m2m_table_name, ['coupon_id', 'order_id'])

        # Removing M2M table for field child_cart on 'Coupon'
        db.delete_table(db.shorten_name('Coupon_child_cart'))

        # Removing M2M table for field child_order on 'Coupon'
        db.delete_table(db.shorten_name('Coupon_child_order'))


        # Changing field 'Coupon.created_at'
        db.alter_column('Coupon', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Coupon.updated_at'
        db.alter_column('Coupon', 'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

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
        u'authModel.user': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'User', 'db_table': "u'UserModel'"},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'carrier': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "u'\\u0423\\u043a\\u0440\\u0430\\u0438\\u043d\\u0430'", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
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
            'settlement': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'cart.cart': {
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'Cart', 'db_table': "u'Cart'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sessionid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authModel.User']", 'null': 'True', 'blank': 'True'})
        },
        u'cart.order': {
            'FIO': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'Meta': {'ordering': "[u'-created_at']", 'object_name': 'Order', 'db_table': "u'Order'"},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'checkbox1': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'checkbox2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Country']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'sessionid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'settlement': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authModel.User']", 'null': 'True', 'blank': 'True'}),
            'warehouse_number': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'coupon.coupon': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Coupon', 'db_table': "'Coupon'"},
            'child_cart': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'Order_child'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['cart.Cart']"}),
            'child_order': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'Order_child'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['cart.Order']"}),
            'coupon_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coupon.CouponGroup']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 11, 0, 0)'}),
            'end_of_the_coupon': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 11, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'3557f2'", 'max_length': '8'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'2015-01-11T22:56:57.389661'", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'number_of_possible_uses': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'number_of_uses': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cart.Order']", 'null': 'True', 'blank': 'True'}),
            'percentage_discount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '10'}),
            'start_of_the_coupon': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 11, 0, 0)'})
        },
        u'coupon.coupongroup': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'CouponGroup', 'db_table': "'CouponGroup'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 11, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'end_of_the_coupon': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 11, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'how_much_coupons': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '10', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'2015-01-11T22:56:57.385125'", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'number_of_possible_uses': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'percentage_discount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '10', 'null': 'True', 'blank': 'True'}),
            'start_of_the_coupon': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 11, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 11, 0, 0)', 'null': 'True', 'blank': 'True'})
        },
        u'product.country': {
            'Meta': {'ordering': "['id']", 'object_name': 'Country', 'db_table': "'Country'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone_code': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('compat.FormSlug.models.ModelSlugField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['coupon']