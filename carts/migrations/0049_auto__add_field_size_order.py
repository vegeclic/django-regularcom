# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Size.order'
        db.add_column('carts_size', 'order',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Size.order'
        db.delete_column('carts_size', 'order')


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
            'newsletter': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'w'"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'accounts.author': {
            'Meta': {'object_name': 'Author'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['accounts.Account']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'null': 'True', 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'})
        },
        'carts.carrier': {
            'Meta': {'object_name': 'Carrier'},
            'apply_suppliers_fee': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'body_de': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'body_fr': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'weight_min': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'carts.carrierlevel': {
            'Meta': {'object_name': 'CarrierLevel', 'unique_together': "(('carrier', 'weight', 'currency'),)"},
            'carrier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Carrier']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Currency']", 'related_name': "'cart_carrier_level_price_currency'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        },
        'carts.content': {
            'Meta': {'object_name': 'Content', 'unique_together': "(('delivery', 'product'),)"},
            'customized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delivery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Delivery']"}),
            'extent': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"})
        },
        'carts.contentproduct': {
            'Meta': {'object_name': 'ContentProduct', 'unique_together': "(('content', 'product'),)"},
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
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'w'"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Subscription']"})
        },
        'carts.extent': {
            'Meta': {'object_name': 'Extent', 'unique_together': "(('subscription', 'product'),)"},
            'customized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extent': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Subscription']"})
        },
        'carts.extentcontent': {
            'Meta': {'object_name': 'ExtentContent'},
            'extent': ('django.db.models.fields.related.ForeignKey', [], {'unique': 'True', 'to': "orm['carts.Extent']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'carts.extentcontentproduct': {
            'Meta': {'object_name': 'ExtentContentProduct', 'unique_together': "(('content', 'product'),)"},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.ExtentContent']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Product']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'carts.price': {
            'Meta': {'object_name': 'Price', 'unique_together': "(('size', 'currency'),)"},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Currency']", 'related_name': "'cart_size_price_currency'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Size']"})
        },
        'carts.size': {
            'Meta': {'object_name': 'Size'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'body_de': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'body_fr': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'null': 'True', 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        },
        'carts.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'carrier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Carrier']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'to': "orm['common.Criteria']", 'related_name': "'cart_subscription_criterias'"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customers.Customer']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'direct_debit': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'frequency': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '2', 'default': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'receive_only_once': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Size']"}),
            'start': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        },
        'carts.thematic': {
            'Meta': {'object_name': 'Thematic'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'body_de': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'body_fr': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'carrier': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['carts.Carrier']"}),
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'to': "orm['common.Criteria']", 'related_name': "'thematic_criterias'"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_duration': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '7'}),
            'end_period': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '7'}),
            'frequency': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locked_carrier': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked_criterias': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked_duration': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked_frequency': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked_products': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked_quantity': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked_receive_only_once': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked_size': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked_start': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'null': 'True', 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'receive_only_once': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['carts.Size']"}),
            'start_duration': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '7'}),
            'start_period': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '10'})
        },
        'carts.thematicextent': {
            'Meta': {'object_name': 'ThematicExtent', 'unique_together': "(('thematic', 'product'),)"},
            'extent': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"}),
            'thematic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Thematic']"})
        },
        'common.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'+'"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Country']"}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'common.criteria': {
            'Meta': {'object_name': 'Criteria'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'})
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
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '200'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'customers.customer': {
            'Meta': {'object_name': 'Customer'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['accounts.Account']"}),
            'billing_address': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['common.Address']", 'unique': 'True', 'null': 'True', 'related_name': "'customer_billing_address'"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_address': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['common.Address']", 'unique': 'True', 'null': 'True', 'related_name': "'customer_main_address'"}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'null': 'True', 'related_name': "'customer_main_image'"}),
            'pro': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'relay_address': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['common.Address']", 'unique': 'True', 'null': 'True', 'related_name': "'customer_relay_address'"}),
            'shipping_address': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['common.Address']", 'unique': 'True', 'null': 'True', 'related_name': "'customer_shipping_address'"})
        },
        'products.category': {
            'Meta': {'object_name': 'Category'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['accounts.Author']", 'null': 'True', 'symmetrical': 'False'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['products.Category']", 'null': 'True', 'related_name': "'categories_rel_+'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'null': 'True', 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'null': 'True', 'max_length': '50'})
        },
        'products.product': {
            'Meta': {'object_name': 'Product'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'body_de': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'body_fr': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'to': "orm['products.Category']", 'related_name': "'+'"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'null': 'True', 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'products_parent': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'to': "orm['products.Product']", 'related_name': "'products_children'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'null': 'True', 'max_length': '50'}),
            'slug_de': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'null': 'True', 'max_length': '50'}),
            'slug_fr': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'null': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"}),
            'tax': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['suppliers.Tax']", 'null': 'True', 'related_name': "'product_price_tax'"})
        },
        'suppliers.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'name_de': ('django.db.models.fields.CharField', [], {'blank': 'True', 'unique': 'True', 'null': 'True', 'max_length': '100'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'blank': 'True', 'unique': 'True', 'null': 'True', 'max_length': '100'})
        },
        'suppliers.price': {
            'Meta': {'object_name': 'Price', 'unique_together': "(('product', 'supplier', 'currency'),)"},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Currency']", 'related_name': "'supplier_product_price_currency'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Product']"}),
            'purchase_price': ('django.db.models.fields.FloatField', [], {}),
            'reference': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '30'}),
            'selling_price': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Supplier']"}),
            'supplier_product_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'tax': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['suppliers.Tax']", 'null': 'True', 'related_name': "'supplier_product_price_tax'"})
        },
        'suppliers.product': {
            'Meta': {'object_name': 'Product'},
            'allergies': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'to': "orm['suppliers.Ingredient']", 'related_name': "'product_allergies'"}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'body_de': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'body_fr': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'brut_ingredients': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'brut_ingredients_de': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'brut_ingredients_fr': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'to': "orm['common.Criteria']", 'related_name': "'product_criterias'"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'null': 'True', 'related_name': "'+'"}),
            'main_price': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['suppliers.Price']", 'unique': 'True', 'null': 'True', 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']", 'related_name': "'product_product'"}),
            'sku': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'slug_de': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'slug_fr': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'to': "orm['suppliers.Supplier']", 'related_name': "'product_suppliers'"}),
            'traces': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'null': 'True', 'to': "orm['suppliers.Ingredient']", 'related_name': "'product_traces'"}),
            'weight': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'})
        },
        'suppliers.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'delivery_delay': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'null': 'True', 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['suppliers.Supplier']", 'null': 'True', 'related_name': "'suppliers_rel_+'"}),
            'threshold_order': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'})
        },
        'suppliers.tax': {
            'Meta': {'object_name': 'Tax'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'rate': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['carts']