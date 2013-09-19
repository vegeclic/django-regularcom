# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Delivery.payed_price'
        db.add_column('carts_delivery', 'payed_price',
                      self.gf('django.db.models.fields.FloatField')(blank=True, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Delivery.payed_price'
        db.delete_column('carts_delivery', 'payed_price')


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
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
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
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'})
        },
        'carts.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['common.Criteria']", 'null': 'True', 'related_name': "'cart_subscription_criterias'"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customers.Customer']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'end': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'frequency': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Size']"}),
            'start': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'v'", 'max_length': '1'})
        },
        'carts.thematic': {
            'Meta': {'object_name': 'Thematic'},
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['common.Criteria']", 'null': 'True', 'related_name': "'thematic_criterias'"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_period': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['products.Product']", 'null': 'True', 'related_name': "'thematic_products'"}),
            'start_period': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True', 'null': 'True'})
        },
        'common.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'+'"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['common.Country']", 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'home_phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'mobile_phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'common.country': {
            'Meta': {'object_name': 'Country'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
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
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'customers.customer': {
            'Meta': {'object_name': 'Customer'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.Account']", 'unique': 'True'}),
            'billing_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Address']", 'unique': 'True', 'null': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Address']", 'unique': 'True', 'null': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'null': 'True'}),
            'shipping_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Address']", 'unique': 'True', 'null': 'True'})
        },
        'products.category': {
            'Meta': {'object_name': 'Category'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['accounts.Author']", 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['products.Category']", 'null': 'True', 'related_name': "'categories_rel_+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True'})
        },
        'products.product': {
            'Meta': {'object_name': 'Product'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['products.Category']", 'null': 'True', 'related_name': "'+'"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'null': 'True'}),
            'products_parent': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['products.Product']", 'null': 'True', 'related_name': "'products_children'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True'}),
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
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['common.Criteria']", 'null': 'True', 'related_name': "'product_criterias'"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'null': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']", 'related_name': "'product_product'"}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'d'", 'max_length': '1'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['suppliers.Supplier']", 'null': 'True', 'related_name': "'product_suppliers'"}),
            'weight': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'})
        },
        'suppliers.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'delivery_delay': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['suppliers.Supplier']", 'null': 'True', 'related_name': "'suppliers_rel_+'"}),
            'threshold_order': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['carts']