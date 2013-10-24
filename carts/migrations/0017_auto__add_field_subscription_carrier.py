# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Subscription.carrier'
        db.add_column('carts_subscription', 'carrier',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['carts.Carrier'], default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Subscription.carrier'
        db.delete_column('carts_subscription', 'carrier_id')


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
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
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Image']", 'blank': 'True', 'null': 'True', 'related_name': "'+'", 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'})
        },
        'carts.carrier': {
            'Meta': {'object_name': 'Carrier'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'carts.carrierlevel': {
            'Meta': {'object_name': 'CarrierLevel'},
            'carrier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Carrier']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Currency']", 'related_name': "'cart_carrier_level_price_currency'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        },
        'carts.carriertranslation': {
            'Meta': {'db_table': "'carts_carrier_translation'", 'unique_together': "[('language_code', 'master')]", 'object_name': 'CarrierTranslation'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Carrier']", 'null': 'True', 'related_name': "'translations'"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'carts.content': {
            'Meta': {'unique_together': "(('delivery', 'extent'),)", 'object_name': 'Content'},
            'delivery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Delivery']"}),
            'extent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Extent']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'carts.contentproduct': {
            'Meta': {'unique_together': "(('content', 'product'),)", 'object_name': 'ContentProduct'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Content']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Product']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'carts.delivery': {
            'Meta': {'object_name': 'Delivery'},
            'date': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payed_price': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'w'", 'max_length': '1'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Subscription']"})
        },
        'carts.extent': {
            'Meta': {'unique_together': "(('subscription', 'product'),)", 'object_name': 'Extent'},
            'extent': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Subscription']"})
        },
        'carts.price': {
            'Meta': {'unique_together': "(('size', 'currency'),)", 'object_name': 'Price'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Currency']", 'related_name': "'cart_size_price_currency'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Size']"})
        },
        'carts.size': {
            'Meta': {'object_name': 'Size'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Image']", 'blank': 'True', 'null': 'True', 'related_name': "'+'", 'unique': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        },
        'carts.sizetranslation': {
            'Meta': {'db_table': "'carts_size_translation'", 'unique_together': "[('language_code', 'master')]", 'object_name': 'SizeTranslation'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Size']", 'null': 'True', 'related_name': "'translations'"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'carts.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'carrier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Carrier']"}),
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['common.Criteria']", 'blank': 'True', 'null': 'True', 'related_name': "'cart_subscription_criterias'", 'symmetrical': 'False'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customers.Customer']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'direct_debit': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'frequency': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Size']"}),
            'start': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        },
        'carts.thematic': {
            'Meta': {'object_name': 'Thematic'},
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['common.Criteria']", 'blank': 'True', 'null': 'True', 'related_name': "'thematic_criterias'", 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_duration': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '7'}),
            'end_period': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '7'}),
            'frequency': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locked_criterias': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked_duration': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked_frequency': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked_products': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked_quantity': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked_size': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked_start': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Image']", 'blank': 'True', 'null': 'True', 'related_name': "'+'", 'unique': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Size']", 'blank': 'True', 'null': 'True'}),
            'start_duration': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '7'}),
            'start_period': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '10'})
        },
        'carts.thematicextent': {
            'Meta': {'unique_together': "(('thematic', 'product'),)", 'object_name': 'ThematicExtent'},
            'extent': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"}),
            'thematic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Thematic']"})
        },
        'carts.thematictranslation': {
            'Meta': {'db_table': "'carts_thematic_translation'", 'unique_together': "[('language_code', 'master')]", 'object_name': 'ThematicTranslation'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Thematic']", 'null': 'True', 'related_name': "'translations'"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'common.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'+'"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Country']", 'blank': 'True', 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '1'}),
            'home_phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'mobile_phone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'postal_code': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'street': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'})
        },
        'common.country': {
            'Meta': {'object_name': 'Country'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'common.criteria': {
            'Meta': {'object_name': 'Criteria'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'common.currency': {
            'Meta': {'object_name': 'Currency'},
            'exchange_rate': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
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
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'customers.customer': {
            'Meta': {'object_name': 'Customer'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.Account']", 'unique': 'True'}),
            'billing_address': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Address']", 'blank': 'True', 'null': 'True', 'related_name': "'+'", 'unique': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_address': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Address']", 'blank': 'True', 'null': 'True', 'related_name': "'+'", 'unique': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Image']", 'blank': 'True', 'null': 'True', 'related_name': "'+'", 'unique': 'True'}),
            'shipping_address': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Address']", 'blank': 'True', 'null': 'True', 'related_name': "'+'", 'unique': 'True'})
        },
        'products.category': {
            'Meta': {'object_name': 'Category'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['accounts.Author']", 'blank': 'True', 'null': 'True', 'symmetrical': 'False'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['products.Category']", 'blank': 'True', 'null': 'True', 'related_name': "'categories_rel_+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Image']", 'blank': 'True', 'null': 'True', 'related_name': "'+'", 'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'products.product': {
            'Meta': {'object_name': 'Product'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['products.Category']", 'blank': 'True', 'null': 'True', 'related_name': "'+'", 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Image']", 'blank': 'True', 'null': 'True', 'related_name': "'+'", 'unique': 'True'}),
            'products_parent': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['products.Product']", 'blank': 'True', 'null': 'True', 'related_name': "'products_children'", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'d'", 'max_length': '1'})
        },
        'products.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tag': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'suppliers.product': {
            'Meta': {'object_name': 'Product'},
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['common.Criteria']", 'blank': 'True', 'null': 'True', 'related_name': "'product_criterias'", 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Image']", 'blank': 'True', 'null': 'True', 'related_name': "'+'", 'unique': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']", 'related_name': "'product_product'"}),
            'sku': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'d'", 'max_length': '1'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['suppliers.Supplier']", 'blank': 'True', 'null': 'True', 'related_name': "'product_suppliers'", 'symmetrical': 'False'}),
            'weight': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'})
        },
        'suppliers.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'delivery_delay': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Image']", 'blank': 'True', 'null': 'True', 'related_name': "'+'", 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['suppliers.Supplier']", 'blank': 'True', 'null': 'True', 'related_name': "'suppliers_rel_+'"}),
            'threshold_order': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['carts']