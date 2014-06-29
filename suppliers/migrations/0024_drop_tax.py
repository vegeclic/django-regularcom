# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ('common', '0010_create_tax'),
    )

    def forwards(self, orm):
        # Changing field 'Price.tax'
        db.alter_column('suppliers_price', 'tax_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Tax'], null=True))

    def backwards(self, orm):
        # Changing field 'Price.tax'
        db.alter_column('suppliers_price', 'tax_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suppliers.Tax'], null=True))

    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'newsletter': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'w'"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'accounts.author': {
            'Meta': {'object_name': 'Author'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.Account']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Image']", 'related_name': "'+'", 'blank': 'True', 'null': 'True', 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        'common.criteria': {
            'Meta': {'object_name': 'Criteria'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'})
        },
        'common.currency': {
            'Meta': {'object_name': 'Currency'},
            'exchange_rate': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True', 'db_index': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'common.image': {
            'Meta': {'object_name': 'Image'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '200'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'common.tax': {
            'Meta': {'object_name': 'Tax'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'rate': ('django.db.models.fields.FloatField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'products.category': {
            'Meta': {'object_name': 'Category'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['accounts.Author']", 'blank': 'True', 'null': 'True', 'symmetrical': 'False'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['products.Category']", 'related_name': "'categories_rel_+'", 'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Image']", 'related_name': "'+'", 'blank': 'True', 'null': 'True', 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True', 'null': 'True'})
        },
        'products.product': {
            'Meta': {'object_name': 'Product'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'body_de': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'body_fr': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['products.Category']", 'related_name': "'+'", 'blank': 'True', 'null': 'True', 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Image']", 'related_name': "'+'", 'blank': 'True', 'null': 'True', 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'products_parent': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['products.Product']", 'related_name': "'products_children'", 'blank': 'True', 'null': 'True', 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True', 'null': 'True'}),
            'slug_de': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True', 'null': 'True'}),
            'slug_fr': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"}),
            'tax': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Tax']", 'related_name': "'product_price_tax'", 'blank': 'True', 'null': 'True'})
        },
        'suppliers.energy': {
            'Meta': {'object_name': 'Energy'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'null': 'True', 'unique': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'null': 'True', 'unique': 'True'})
        },
        'suppliers.energyextent': {
            'Meta': {'object_name': 'EnergyExtent'},
            'energy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Energy']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'})
        },
        'suppliers.entry': {
            'Meta': {'object_name': 'Entry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Order']"}),
            'product': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suppliers.Product']", 'unique': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'})
        },
        'suppliers.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'null': 'True', 'unique': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'null': 'True', 'unique': 'True'})
        },
        'suppliers.ingredientextent': {
            'Meta': {'object_name': 'IngredientExtent'},
            'bio': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extent': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Ingredient']"}),
            'ingredient_parent': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['suppliers.IngredientExtent']", 'related_name': "'ingredient_children'", 'blank': 'True', 'null': 'True', 'symmetrical': 'False'})
        },
        'suppliers.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suppliers.Product']", 'unique': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Store']"})
        },
        'suppliers.order': {
            'Meta': {'object_name': 'Order'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"})
        },
        'suppliers.price': {
            'Meta': {'object_name': 'Price', 'unique_together': "(('product', 'supplier', 'currency'),)"},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Currency']", 'related_name': "'supplier_product_price_currency'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Product']"}),
            'purchase_price': ('django.db.models.fields.FloatField', [], {}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True', 'null': 'True'}),
            'selling_price': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Supplier']"}),
            'supplier_product_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'tax': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Tax']", 'related_name': "'supplier_product_price_tax'", 'blank': 'True', 'null': 'True'})
        },
        'suppliers.product': {
            'Meta': {'object_name': 'Product'},
            'allergies': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['suppliers.Ingredient']", 'related_name': "'product_allergies'", 'blank': 'True', 'null': 'True', 'symmetrical': 'False'}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'body_de': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'body_fr': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'brut_ingredients': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'brut_ingredients_de': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'brut_ingredients_fr': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['common.Criteria']", 'related_name': "'product_criterias'", 'blank': 'True', 'null': 'True', 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Image']", 'related_name': "'+'", 'blank': 'True', 'null': 'True', 'unique': 'True'}),
            'main_price': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suppliers.Price']", 'related_name': "'+'", 'blank': 'True', 'null': 'True', 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']", 'related_name': "'product_product'"}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'slug_de': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'slug_fr': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['suppliers.Supplier']", 'related_name': "'product_suppliers'", 'blank': 'True', 'null': 'True', 'symmetrical': 'False'}),
            'traces': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['suppliers.Ingredient']", 'related_name': "'product_traces'", 'blank': 'True', 'null': 'True', 'symmetrical': 'False'}),
            'weight': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'})
        },
        'suppliers.store': {
            'Meta': {'object_name': 'Store'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'})
        },
        'suppliers.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'delivery_delay': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Image']", 'related_name': "'+'", 'blank': 'True', 'null': 'True', 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['suppliers.Supplier']", 'related_name': "'suppliers_rel_+'", 'blank': 'True', 'null': 'True'}),
            'threshold_order': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'})
        },
        'suppliers.supplierfee': {
            'Meta': {'object_name': 'SupplierFee', 'unique_together': "(('supplier', 'currency'),)"},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Currency']", 'related_name': "'supplier_fee_currency'"}),
            'fee_per_weight': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Supplier']"})
        }
    }

    complete_apps = ['suppliers']
