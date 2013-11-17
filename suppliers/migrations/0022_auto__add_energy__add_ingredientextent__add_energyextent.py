# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Energy'
        db.create_table('suppliers_energy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('name_de', self.gf('django.db.models.fields.CharField')(null=True, unique=True, blank=True, max_length=100)),
            ('name_fr', self.gf('django.db.models.fields.CharField')(null=True, unique=True, blank=True, max_length=100)),
        ))
        db.send_create_signal('suppliers', ['Energy'])

        # Adding model 'IngredientExtent'
        db.create_table('suppliers_ingredientextent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suppliers.Ingredient'])),
            ('extent', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('bio', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('suppliers', ['IngredientExtent'])

        # Adding M2M table for field ingredient_parent on 'IngredientExtent'
        m2m_table_name = db.shorten_name('suppliers_ingredientextent_ingredient_parent')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_ingredientextent', models.ForeignKey(orm['suppliers.ingredientextent'], null=False)),
            ('to_ingredientextent', models.ForeignKey(orm['suppliers.ingredientextent'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_ingredientextent_id', 'to_ingredientextent_id'])

        # Adding model 'EnergyExtent'
        db.create_table('suppliers_energyextent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('energy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suppliers.Energy'], unique=True)),
            ('value', self.gf('django.db.models.fields.CharField')(null=True, max_length=200, blank=True)),
        ))
        db.send_create_signal('suppliers', ['EnergyExtent'])

        # Removing M2M table for field ingredients on 'Product'
        db.delete_table(db.shorten_name('suppliers_product_ingredients'))

        # Adding M2M table for field allergies on 'Product'
        m2m_table_name = db.shorten_name('suppliers_product_allergies')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['suppliers.product'], null=False)),
            ('ingredient', models.ForeignKey(orm['suppliers.ingredient'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'ingredient_id'])

        # Adding M2M table for field traces on 'Product'
        m2m_table_name = db.shorten_name('suppliers_product_traces')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['suppliers.product'], null=False)),
            ('ingredient', models.ForeignKey(orm['suppliers.ingredient'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'ingredient_id'])


    def backwards(self, orm):
        # Deleting model 'Energy'
        db.delete_table('suppliers_energy')

        # Deleting model 'IngredientExtent'
        db.delete_table('suppliers_ingredientextent')

        # Removing M2M table for field ingredient_parent on 'IngredientExtent'
        db.delete_table(db.shorten_name('suppliers_ingredientextent_ingredient_parent'))

        # Deleting model 'EnergyExtent'
        db.delete_table('suppliers_energyextent')

        # Adding M2M table for field ingredients on 'Product'
        m2m_table_name = db.shorten_name('suppliers_product_ingredients')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['suppliers.product'], null=False)),
            ('ingredient', models.ForeignKey(orm['suppliers.ingredient'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'ingredient_id'])

        # Removing M2M table for field allergies on 'Product'
        db.delete_table(db.shorten_name('suppliers_product_allergies'))

        # Removing M2M table for field traces on 'Product'
        db.delete_table(db.shorten_name('suppliers_product_traces'))


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
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
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.Account']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'related_name': "'+'", 'to': "orm['common.Image']", 'unique': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'})
        },
        'common.criteria': {
            'Meta': {'object_name': 'Criteria'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'})
        },
        'common.currency': {
            'Meta': {'object_name': 'Currency'},
            'exchange_rate': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'unique': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'common.image': {
            'Meta': {'object_name': 'Image'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '200'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'products.category': {
            'Meta': {'object_name': 'Category'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'to': "orm['accounts.Author']", 'blank': 'True', 'symmetrical': 'False'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'categories_rel_+'", 'to': "orm['products.Category']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'related_name': "'+'", 'to': "orm['common.Image']", 'unique': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'null': 'True', 'max_length': '50', 'blank': 'True'})
        },
        'products.product': {
            'Meta': {'object_name': 'Product'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'body_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'+'", 'to': "orm['products.Category']", 'blank': 'True', 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'related_name': "'+'", 'to': "orm['common.Image']", 'unique': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'products_parent': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'products_children'", 'to': "orm['products.Product']", 'blank': 'True', 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'null': 'True', 'max_length': '50', 'blank': 'True'}),
            'slug_de': ('django.db.models.fields.SlugField', [], {'null': 'True', 'max_length': '50', 'blank': 'True'}),
            'slug_fr': ('django.db.models.fields.SlugField', [], {'null': 'True', 'max_length': '50', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"}),
            'tax': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'product_price_tax'", 'to': "orm['suppliers.Tax']", 'blank': 'True'})
        },
        'products.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tag': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'suppliers.energy': {
            'Meta': {'object_name': 'Energy'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'null': 'True', 'unique': 'True', 'blank': 'True', 'max_length': '100'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'null': 'True', 'unique': 'True', 'blank': 'True', 'max_length': '100'})
        },
        'suppliers.energyextent': {
            'Meta': {'object_name': 'EnergyExtent'},
            'energy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Energy']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'})
        },
        'suppliers.entry': {
            'Meta': {'object_name': 'Entry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Order']"}),
            'product': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suppliers.Product']", 'unique': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'suppliers.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'null': 'True', 'unique': 'True', 'blank': 'True', 'max_length': '100'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'null': 'True', 'unique': 'True', 'blank': 'True', 'max_length': '100'})
        },
        'suppliers.ingredientextent': {
            'Meta': {'object_name': 'IngredientExtent'},
            'bio': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extent': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Ingredient']"}),
            'ingredient_parent': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'ingredient_children'", 'to': "orm['suppliers.IngredientExtent']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'suppliers.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['suppliers.Product']", 'unique': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'Meta': {'object_name': 'Price', 'unique_together': "(('product', 'supplier', 'currency'),)"},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Currency']", 'related_name': "'supplier_product_price_currency'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Product']"}),
            'purchase_price': ('django.db.models.fields.FloatField', [], {}),
            'reference': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '30', 'blank': 'True'}),
            'selling_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Supplier']"}),
            'supplier_product_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'tax': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'supplier_product_price_tax'", 'to': "orm['suppliers.Tax']", 'blank': 'True'})
        },
        'suppliers.product': {
            'Meta': {'object_name': 'Product'},
            'allergies': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'product_allergies'", 'to': "orm['suppliers.Ingredient']", 'blank': 'True', 'symmetrical': 'False'}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'body_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'product_criterias'", 'to': "orm['common.Criteria']", 'blank': 'True', 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'related_name': "'+'", 'to': "orm['common.Image']", 'unique': 'True', 'blank': 'True'}),
            'main_price': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'related_name': "'+'", 'to': "orm['suppliers.Price']", 'unique': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'old_ingredients': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'old_ingredients_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'old_ingredients_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']", 'related_name': "'product_product'"}),
            'sku': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'slug_de': ('django.db.models.fields.SlugField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'slug_fr': ('django.db.models.fields.SlugField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'product_suppliers'", 'to': "orm['suppliers.Supplier']", 'blank': 'True', 'symmetrical': 'False'}),
            'traces': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'product_traces'", 'to': "orm['suppliers.Ingredient']", 'blank': 'True', 'symmetrical': 'False'}),
            'weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'suppliers.store': {
            'Meta': {'object_name': 'Store'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'suppliers.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'delivery_delay': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'related_name': "'+'", 'to': "orm['common.Image']", 'unique': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'suppliers_rel_+'", 'to': "orm['suppliers.Supplier']", 'blank': 'True'}),
            'threshold_order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'suppliers.supplierfee': {
            'Meta': {'object_name': 'SupplierFee', 'unique_together': "(('supplier', 'currency'),)"},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Currency']", 'related_name': "'supplier_fee_currency'"}),
            'fee_per_weight': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Supplier']"})
        },
        'suppliers.tax': {
            'Meta': {'object_name': 'Tax'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'rate': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['suppliers']