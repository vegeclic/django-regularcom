# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Product.slug'
        db.delete_column('suppliers_product', 'slug')


    def backwards(self, orm):
        # Adding field 'Product.slug'
        db.add_column('suppliers_product', 'slug',
                      self.gf('django.db.models.fields.SlugField')(max_length=100, unique=True, default=''),
                      keep_default=False)


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'max_length': '255', 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'accounts.author': {
            'Meta': {'object_name': 'Author'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['accounts.Account']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'blank': 'True', 'unique': 'True', 'related_name': "'+'", 'to': "orm['common.Image']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        'common.criteria': {
            'Meta': {'object_name': 'Criteria'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'common.currency': {
            'Meta': {'object_name': 'Currency'},
            'exchange_rate': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'unique': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'common.image': {
            'Meta': {'object_name': 'Image'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '200'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'products.category': {
            'Meta': {'object_name': 'Category'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'blank': 'True', 'to': "orm['accounts.Author']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'blank': 'True', 'related_name': "'categories_rel_+'", 'to': "orm['products.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'blank': 'True', 'unique': 'True', 'related_name': "'+'", 'to': "orm['common.Image']"})
        },
        'products.product': {
            'Meta': {'object_name': 'Product'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'blank': 'True', 'symmetrical': 'False', 'related_name': "'+'", 'to': "orm['products.Category']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'blank': 'True', 'unique': 'True', 'related_name': "'+'", 'to': "orm['common.Image']"}),
            'products_parent': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'blank': 'True', 'symmetrical': 'False', 'related_name': "'products_children'", 'to': "orm['products.Product']"}),
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
            'product': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['suppliers.Product']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'suppliers.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['suppliers.Product']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Store']"})
        },
        'suppliers.order': {
            'Meta': {'object_name': 'Order'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"})
        },
        'suppliers.price': {
            'Meta': {'unique_together': "(('product', 'supplier', 'currency'),)", 'object_name': 'Price'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supplier_product_price_currency'", 'to': "orm['common.Currency']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Product']"}),
            'purchase_price': ('django.db.models.fields.FloatField', [], {}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'selling_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Supplier']"}),
            'supplier_product_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'tax': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'related_name': "'supplier_product_price_tax'", 'to': "orm['suppliers.Tax']"})
        },
        'suppliers.product': {
            'Meta': {'object_name': 'Product'},
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'blank': 'True', 'symmetrical': 'False', 'related_name': "'product_criterias'", 'to': "orm['common.Criteria']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'blank': 'True', 'unique': 'True', 'related_name': "'+'", 'to': "orm['common.Image']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product_product'", 'to': "orm['products.Product']"}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'blank': 'True', 'symmetrical': 'False', 'related_name': "'product_suppliers'", 'to': "orm['suppliers.Supplier']"}),
            'weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'suppliers.producttranslation': {
            'Meta': {'db_table': "'suppliers_product_translation'", 'unique_together': "[('language_code', 'master')]", 'object_name': 'ProductTranslation'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'translations'", 'to': "orm['suppliers.Product']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'new_slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'suppliers.store': {
            'Meta': {'object_name': 'Store'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'})
        },
        'suppliers.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'delivery_delay': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'blank': 'True', 'unique': 'True', 'related_name': "'+'", 'to': "orm['common.Image']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'blank': 'True', 'related_name': "'suppliers_rel_+'", 'to': "orm['suppliers.Supplier']"}),
            'threshold_order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'suppliers.supplierfee': {
            'Meta': {'unique_together': "(('supplier', 'currency'),)", 'object_name': 'SupplierFee'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supplier_fee_currency'", 'to': "orm['common.Currency']"}),
            'fee_per_weight': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Supplier']"})
        },
        'suppliers.tax': {
            'Meta': {'object_name': 'Tax'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rate': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['suppliers']