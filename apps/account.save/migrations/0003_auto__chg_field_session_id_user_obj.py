# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Changing field 'Product.user_obj'
        db.alter_column('Session_ID', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['authModel.User'], null=True))

    def backwards(self, orm):
        # Changing field 'Product.user_obj'
        db.alter_column('Session_ID', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True))

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
        },
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
        },
        u'product.additional_information': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Additional_Information', 'db_table': "'Additional_Information'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'information'", 'to': u"orm['product.Product']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.additionalinformationforprice': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'AdditionalInformationForPrice', 'db_table': "'AdditionalInformationForPrice'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['product.InformationForPrice']", 'symmetrical': 'False'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'additionalinformationforprice'", 'to': u"orm['product.Product']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.category': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Category', 'db_table': "'Category'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'font_px': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '14'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'item_description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '190', 'null': 'True', 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'max_length': '190', 'null': 'True', 'blank': 'True'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': u"orm['product.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'serial_number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'shown_bold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shown_colored': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shown_italic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('compat.FormSlug.models.ModelSlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'user_obj': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authModel.User']", 'null': 'True', 'blank': 'True'}),
            'visibility': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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
        },
        u'product.currency': {
            'Meta': {'ordering': "['id']", 'object_name': 'Currency', 'db_table': "'Currency'"},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['product.Country']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '12', 'decimal_places': '5'}),
            'exchange_rate': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '12', 'decimal_places': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'name_truncated': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.discount': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Discount', 'db_table': "'Discount'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percent': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'discount'", 'to': u"orm['product.Product']"}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.extendedprice': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'ExtendedPrice', 'db_table': "u'ExtendedPrice'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['product.InformationForPrice']", 'symmetrical': 'False'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'extendedprice'", 'to': u"orm['product.Product']"}),
            'regular_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.information': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Information', 'db_table': "'Information'"},
            'additional_information': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Additional_Information']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.informationforprice': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'InformationForPrice', 'db_table': "'InformationForPrice'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'informationforprice'", 'null': 'True', 'to': u"orm['product.Product']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.intermediatemodelmanufacturer': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'IntermediateModelManufacturer', 'db_table': "'IntermediateModelManufacturer'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'related_Manufacturer'", 'to': u"orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Manufacturer']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.itemid': {
            'ItemID': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'Meta': {'ordering': "['-created_at']", 'object_name': 'ItemID', 'db_table': "'ItemID'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_ItemID'", 'to': u"orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.manufacturer': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Manufacturer', 'db_table': "'Manufacturer'"},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['product.Country']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter_to_article': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.photo': {
            'Meta': {'ordering': "['serial_number', '-created_at']", 'object_name': 'Photo', 'db_table': "'Photo'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_Photo'", 'to': u"orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'meta_alt': ('django.db.models.fields.CharField', [], {'max_length': '190', 'null': 'True', 'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'max_length': '190', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'photo': ('compat.ImageWithThumbs.models.ImageWithThumbsField', [], {'max_length': '100'}),
            'serial_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'sign': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.product': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Product', 'db_table': "'Product'"},
            'action': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['discount.Action']", 'null': 'True', 'db_table': "'Product_to_Action'", 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'products'", 'symmetrical': 'False', 'to': u"orm['product.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['product.Currency']"}),
            'datetime_pub': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'disclose_product': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_main_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_availability': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'is_bestseller': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item_description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '190', 'null': 'True', 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'max_length': '190', 'null': 'True', 'blank': 'True'}),
            'minimal_quantity': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '8', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'price_of_quantity': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '15', 'decimal_places': '5'}),
            'quantity_of_complete': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '8', 'decimal_places': '2'}),
            'recommended': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'Product'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['product.Product']"}),
            'regular_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'serial_number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'unit_of_measurement': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Unit_of_Measurement']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('compat.FormSlug.models.ModelSlugField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user_obj': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authModel.User']", 'null': 'True', 'blank': 'True'}),
            'visibility': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'})
        },
        u'product.unit_of_measurement': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Unit_of_Measurement', 'db_table': "u'Unit_of_Measurement'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u'\\u0448\\u0442.'", 'max_length': '64'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.view': {
            'Meta': {'ordering': "['-updated_at']", 'object_name': 'View', 'db_table': "'View'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'related_View'", 'to': u"orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'product.viewed': {
            'Meta': {'ordering': "['-updated_at']", 'object_name': 'Viewed', 'db_table': "'Viewed'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'related_Viewed'", 'to': u"orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_viewed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 16, 0, 0)'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'sessionid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_obj': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['authModel.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['account']