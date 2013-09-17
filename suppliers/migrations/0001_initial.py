# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Supplier'
        db.create_table('suppliers_supplier', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
            ('delivery_delay', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
            ('threshold_order', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
            ('main_image', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, blank=True, null=True, to=orm['common.Image'], related_name='+')),
        ))
        db.send_create_signal('suppliers', ['Supplier'])

        # Adding M2M table for field suppliers on 'Supplier'
        m2m_table_name = db.shorten_name('suppliers_supplier_suppliers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_supplier', models.ForeignKey(orm['suppliers.supplier'], null=False)),
            ('to_supplier', models.ForeignKey(orm['suppliers.supplier'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_supplier_id', 'to_supplier_id'])

        # Adding model 'ProductTranslation'
        db.create_table('suppliers_product_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ingredients', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suppliers.Product'], null=True, related_name='translations')),
        ))
        db.send_create_signal('suppliers', ['ProductTranslation'])

        # Adding unique constraint on 'ProductTranslation', fields ['language_code', 'master']
        db.create_unique('suppliers_product_translation', ['language_code', 'master_id'])

        # Adding model 'Product'
        db.create_table('suppliers_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, unique=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Product'], related_name='+')),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1, default='d')),
            ('weight', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('sku', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('main_image', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, blank=True, null=True, to=orm['common.Image'], related_name='+')),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('date_last_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
        ))
        db.send_create_signal('suppliers', ['Product'])

        # Adding M2M table for field suppliers on 'Product'
        m2m_table_name = db.shorten_name('suppliers_product_suppliers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['suppliers.product'], null=False)),
            ('supplier', models.ForeignKey(orm['suppliers.supplier'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'supplier_id'])

        # Adding M2M table for field criterias on 'Product'
        m2m_table_name = db.shorten_name('suppliers_product_criterias')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['suppliers.product'], null=False)),
            ('criteria', models.ForeignKey(orm['common.criteria'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'criteria_id'])

        # Adding model 'Price'
        db.create_table('suppliers_price', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suppliers.Product'])),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suppliers.Supplier'])),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True, null=True)),
            ('supplier_product_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True, null=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Currency'], related_name='supplier_product_price_currency')),
            ('purchase_price', self.gf('django.db.models.fields.FloatField')()),
            ('selling_price', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
        ))
        db.send_create_signal('suppliers', ['Price'])

        # Adding unique constraint on 'Price', fields ['product', 'supplier', 'currency']
        db.create_unique('suppliers_price', ['product_id', 'supplier_id', 'currency_id'])

        # Adding model 'Inventory'
        db.create_table('suppliers_inventory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suppliers.Store'])),
            ('product', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['suppliers.Product'], unique=True)),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('date_last_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
        ))
        db.send_create_signal('suppliers', ['Inventory'])

        # Adding model 'Store'
        db.create_table('suppliers_store', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('date_last_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
        ))
        db.send_create_signal('suppliers', ['Store'])

        # Adding model 'Entry'
        db.create_table('suppliers_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suppliers.Order'])),
            ('product', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['suppliers.Product'], unique=True)),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True, null=True)),
        ))
        db.send_create_signal('suppliers', ['Entry'])

        # Adding model 'Order'
        db.create_table('suppliers_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1, default='d')),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('date_last_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
        ))
        db.send_create_signal('suppliers', ['Order'])


    def backwards(self, orm):
        # Removing unique constraint on 'Price', fields ['product', 'supplier', 'currency']
        db.delete_unique('suppliers_price', ['product_id', 'supplier_id', 'currency_id'])

        # Removing unique constraint on 'ProductTranslation', fields ['language_code', 'master']
        db.delete_unique('suppliers_product_translation', ['language_code', 'master_id'])

        # Deleting model 'Supplier'
        db.delete_table('suppliers_supplier')

        # Removing M2M table for field suppliers on 'Supplier'
        db.delete_table(db.shorten_name('suppliers_supplier_suppliers'))

        # Deleting model 'ProductTranslation'
        db.delete_table('suppliers_product_translation')

        # Deleting model 'Product'
        db.delete_table('suppliers_product')

        # Removing M2M table for field suppliers on 'Product'
        db.delete_table(db.shorten_name('suppliers_product_suppliers'))

        # Removing M2M table for field criterias on 'Product'
        db.delete_table(db.shorten_name('suppliers_product_criterias'))

        # Deleting model 'Price'
        db.delete_table('suppliers_price')

        # Deleting model 'Inventory'
        db.delete_table('suppliers_inventory')

        # Deleting model 'Store'
        db.delete_table('suppliers_store')

        # Deleting model 'Entry'
        db.delete_table('suppliers_entry')

        # Deleting model 'Order'
        db.delete_table('suppliers_order')


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'accounts.author': {
            'Meta': {'object_name': 'Author'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.Account']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        'common.criteria': {
            'Meta': {'object_name': 'Criteria'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'})
        },
        'common.currency': {
            'Meta': {'object_name': 'Currency'},
            'exchange_rate': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'common.image': {
            'Meta': {'object_name': 'Image'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '200'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'products.category': {
            'Meta': {'object_name': 'Category'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'null': 'True', 'to': "orm['accounts.Author']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'related_name': "'+'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'products.product': {
            'Meta': {'object_name': 'Product'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'null': 'True', 'to': "orm['products.Category']", 'related_name': "'+'"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'related_name': "'+'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"})
        },
        'products.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tag': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'suppliers.entry': {
            'Meta': {'object_name': 'Entry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Order']"}),
            'product': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suppliers.Product']", 'unique': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'})
        },
        'suppliers.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suppliers.Product']", 'unique': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Store']"})
        },
        'suppliers.order': {
            'Meta': {'object_name': 'Order'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"})
        },
        'suppliers.price': {
            'Meta': {'unique_together': "(('product', 'supplier', 'currency'),)", 'object_name': 'Price'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Currency']", 'related_name': "'supplier_product_price_currency'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Product']"}),
            'purchase_price': ('django.db.models.fields.FloatField', [], {}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True', 'null': 'True'}),
            'selling_price': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Supplier']"}),
            'supplier_product_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'})
        },
        'suppliers.product': {
            'Meta': {'object_name': 'Product'},
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'null': 'True', 'to': "orm['common.Criteria']", 'related_name': "'product_criterias'"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'related_name': "'+'"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']", 'related_name': "'+'"}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'null': 'True', 'to': "orm['suppliers.Supplier']", 'related_name': "'product_suppliers'"}),
            'weight': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'})
        },
        'suppliers.producttranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'ProductTranslation', 'db_table': "'suppliers_product_translation'"},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Product']", 'null': 'True', 'related_name': "'translations'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'})
        },
        'suppliers.store': {
            'Meta': {'object_name': 'Store'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'})
        },
        'suppliers.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'delivery_delay': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'to': "orm['suppliers.Supplier']", 'related_name': "'suppliers_rel_+'"}),
            'threshold_order': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['suppliers']