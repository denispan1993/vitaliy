# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('Category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name=u'children', null=True, to=orm['product.Category'])),
            ('serial_number', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('shown_colored', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('shown_bold', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('shown_italic', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('url', self.gf('compat.FormSlug.models.ModelSlugField')(max_length=50, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('meta_title', self.gf('django.db.models.fields.CharField')(max_length=190, null=True, blank=True)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=190, null=True, blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(max_length=160, null=True, blank=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('visibility', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('mptt_level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'product', ['Category'])

        # Adding model 'Product'
        db.create_table('Product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('disclose_product', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('in_main_page', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_bestseller', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('url', self.gf('compat.FormSlug.models.ModelSlugField')(db_index=True, max_length=255, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('item_description', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('minimal_quantity', self.gf('django.db.models.fields.DecimalField')(default=1, max_digits=8, decimal_places=2)),
            ('quantity_of_complete', self.gf('django.db.models.fields.DecimalField')(default=1, max_digits=8, decimal_places=2)),
            ('weight', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=8, decimal_places=2, blank=True)),
            ('unit_of_measurement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['product.Unit_of_Measurement'])),
            ('is_availability', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('regular_price', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=8, decimal_places=2, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2)),
            ('price_of_quantity', self.gf('django.db.models.fields.DecimalField')(default=1, max_digits=15, decimal_places=5)),
            ('datetime_pub', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('meta_title', self.gf('django.db.models.fields.CharField')(max_length=190, null=True, blank=True)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=190, null=True, blank=True)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(max_length=160, null=True, blank=True)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('visibility', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'product', ['Product'])

        # Adding M2M table for field category on 'Product'
        m2m_table_name = db.shorten_name('Product_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm[u'product.product'], null=False)),
            ('category', models.ForeignKey(orm[u'product.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'category_id'])

        # Adding M2M table for field recomendate on 'Product'
        m2m_table_name = db.shorten_name('Product_recomendate')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_product', models.ForeignKey(orm[u'product.product'], null=False)),
            ('to_product', models.ForeignKey(orm[u'product.product'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_product_id', 'to_product_id'])

        # Adding model 'ItemID'
        db.create_table('ItemID', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_ItemID', to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('ItemID', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'product', ['ItemID'])

        # Adding model 'IntermediateModelManufacturer'
        db.create_table('IntermediateModelManufacturer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='related_Manufacturer', to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True)),
            ('key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['product.Manufacturer'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'product', ['IntermediateModelManufacturer'])

        # Adding model 'Manufacturer'
        db.create_table('Manufacturer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('letter_to_article', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'product', ['Manufacturer'])

        # Adding model 'Additional_Information'
        db.create_table('Additional_Information', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'information', to=orm['product.Product'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'product', ['Additional_Information'])

        # Adding model 'Information'
        db.create_table('Information', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('additional_information', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['product.Additional_Information'])),
            ('information', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'product', ['Information'])

        # Adding model 'Unit_of_Measurement'
        db.create_table(u'Unit_of_Measurement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=u'\u0448\u0442.', max_length=64)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'product', ['Unit_of_Measurement'])

        # Adding model 'Discount'
        db.create_table('Discount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'discount', to=orm['product.Product'])),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=2)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=8, decimal_places=2, blank=True)),
            ('percent', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'product', ['Discount'])

        # Adding model 'Photo'
        db.create_table('Photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='related_Photo', to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('serial_number', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('main', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('photo', self.gf('compat.ImageWithThumbs.models.ImageWithThumbsField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('sign', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('meta_title', self.gf('django.db.models.fields.CharField')(max_length=190, null=True, blank=True)),
            ('meta_alt', self.gf('django.db.models.fields.CharField')(max_length=190, null=True, blank=True)),
        ))
        db.send_create_signal(u'product', ['Photo'])

        # Adding model 'Country'
        db.create_table('Country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone_code', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('url', self.gf('compat.FormSlug.models.ModelSlugField')(db_index=True, max_length=255, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'product', ['Country'])

        # Adding model 'View'
        db.create_table('View', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='related_View', to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True)),
            ('view_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'product', ['View'])

        # Adding model 'Viewed'
        db.create_table('Viewed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='related_Viewed', to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True)),
            ('user_obj', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('sessionid', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('last_viewed', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 27, 0, 0))),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'product', ['Viewed'])

        # Adding model 'InformationForPrice'
        db.create_table('InformationForPrice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='informationforprice', null=True, to=orm['product.Product'])),
            ('information', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'product', ['InformationForPrice'])

        # Adding model 'ExtendedPrice'
        db.create_table(u'ExtendedPrice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='extendedprice', to=orm['product.Product'])),
            ('regular_price', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=10, decimal_places=2, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'product', ['ExtendedPrice'])

        # Adding M2M table for field information on 'ExtendedPrice'
        m2m_table_name = db.shorten_name(u'ExtendedPrice_information')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('extendedprice', models.ForeignKey(orm[u'product.extendedprice'], null=False)),
            ('informationforprice', models.ForeignKey(orm[u'product.informationforprice'], null=False))
        ))
        db.create_unique(m2m_table_name, ['extendedprice_id', 'informationforprice_id'])

        # Adding model 'AdditionalInformationForPrice'
        db.create_table('AdditionalInformationForPrice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='additionalinformationforprice', to=orm['product.Product'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'product', ['AdditionalInformationForPrice'])

        # Adding M2M table for field information on 'AdditionalInformationForPrice'
        m2m_table_name = db.shorten_name('AdditionalInformationForPrice_information')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('additionalinformationforprice', models.ForeignKey(orm[u'product.additionalinformationforprice'], null=False)),
            ('informationforprice', models.ForeignKey(orm[u'product.informationforprice'], null=False))
        ))
        db.create_unique(m2m_table_name, ['additionalinformationforprice_id', 'informationforprice_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('Category')

        # Deleting model 'Product'
        db.delete_table('Product')

        # Removing M2M table for field category on 'Product'
        db.delete_table(db.shorten_name('Product_category'))

        # Removing M2M table for field recomendate on 'Product'
        db.delete_table(db.shorten_name('Product_recomendate'))

        # Deleting model 'ItemID'
        db.delete_table('ItemID')

        # Deleting model 'IntermediateModelManufacturer'
        db.delete_table('IntermediateModelManufacturer')

        # Deleting model 'Manufacturer'
        db.delete_table('Manufacturer')

        # Deleting model 'Additional_Information'
        db.delete_table('Additional_Information')

        # Deleting model 'Information'
        db.delete_table('Information')

        # Deleting model 'Unit_of_Measurement'
        db.delete_table(u'Unit_of_Measurement')

        # Deleting model 'Discount'
        db.delete_table('Discount')

        # Deleting model 'Photo'
        db.delete_table('Photo')

        # Deleting model 'Country'
        db.delete_table('Country')

        # Deleting model 'View'
        db.delete_table('View')

        # Deleting model 'Viewed'
        db.delete_table('Viewed')

        # Deleting model 'InformationForPrice'
        db.delete_table('InformationForPrice')

        # Deleting model 'ExtendedPrice'
        db.delete_table(u'ExtendedPrice')

        # Removing M2M table for field information on 'ExtendedPrice'
        db.delete_table(db.shorten_name(u'ExtendedPrice_information'))

        # Deleting model 'AdditionalInformationForPrice'
        db.delete_table('AdditionalInformationForPrice')

        # Removing M2M table for field information on 'AdditionalInformationForPrice'
        db.delete_table(db.shorten_name('AdditionalInformationForPrice_information'))


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'Meta': {'ordering': "['serial_number', '-created_at']", 'object_name': 'Category', 'db_table': "'Category'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter_to_article': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.photo': {
            'Meta': {'ordering': "['serial_number']", 'object_name': 'Photo', 'db_table': "'Photo'"},
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
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "u'products'", 'symmetrical': 'False', 'to': u"orm['product.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datetime_pub': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'disclose_product': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_main_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_availability': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'is_bestseller': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item_description': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '190', 'null': 'True', 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'meta_title': ('django.db.models.fields.CharField', [], {'max_length': '190', 'null': 'True', 'blank': 'True'}),
            'minimal_quantity': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '8', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'price_of_quantity': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '15', 'decimal_places': '5'}),
            'quantity_of_complete': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '8', 'decimal_places': '2'}),
            'recomendate': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'recommended'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['product.Product']"}),
            'regular_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'unit_of_measurement': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Unit_of_Measurement']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('compat.FormSlug.models.ModelSlugField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'last_viewed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 27, 0, 0)'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'sessionid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_obj': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['product']