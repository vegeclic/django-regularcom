# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Content', fields ['delivery', 'extent']
        db.delete_unique('carts_content', ['delivery_id', 'extent_id'])

        # Deleting field 'Content.extent'
        db.delete_column('carts_content', 'extent_id')


        # Changing field 'Content.product'
        db.alter_column('carts_content', 'product_id', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['products.Product']))
        # Adding unique constraint on 'Content', fields ['delivery', 'product']
        db.create_unique('carts_content', ['delivery_id', 'product_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Content', fields ['delivery', 'product']
        db.delete_unique('carts_content', ['delivery_id', 'product_id'])

        # Adding field 'Content.extent'
        db.add_column('carts_content', 'extent',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['carts.Extent']),
                      keep_default=False)


        # Changing field 'Content.product'
        db.alter_column('carts_content', 'product_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['products.Product']))
        # Adding unique constraint on 'Content', fields ['delivery', 'extent']
        db.create_unique('carts_content', ['delivery_id', 'extent_id'])


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '255'}),
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
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Image']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        'carts.carrier': {
            'Meta': {'object_name': 'Carrier'},
            'apply_suppliers_fee': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'weight_min': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'carts.carrierlevel': {
            'Meta': {'unique_together': "(('carrier', 'weight', 'currency'),)", 'object_name': 'CarrierLevel'},
            'carrier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Carrier']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cart_carrier_level_price_currency'", 'to': "orm['common.Currency']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        },
        'carts.carriertranslation': {
            'Meta': {'db_table': "'carts_carrier_translation'", 'unique_together': "[('language_code', 'master')]", 'object_name': 'CarrierTranslation'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'translations'", 'to': "orm['carts.Carrier']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'carts.content': {
            'Meta': {'unique_together': "(('delivery', 'product'),)", 'object_name': 'Content'},
            'customized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delivery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Delivery']"}),
            'extent_value': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"})
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
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payed_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'w'"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Subscription']"})
        },
        'carts.extent': {
            'Meta': {'unique_together': "(('subscription', 'product'),)", 'object_name': 'Extent'},
            'customized': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extent': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Subscription']"})
        },
        'carts.extentcontent': {
            'Meta': {'object_name': 'ExtentContent'},
            'extent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Extent']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'carts.extentcontentproduct': {
            'Meta': {'unique_together': "(('content', 'product'),)", 'object_name': 'ExtentContentProduct'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.ExtentContent']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['suppliers.Product']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'carts.price': {
            'Meta': {'unique_together': "(('size', 'currency'),)", 'object_name': 'Price'},
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cart_size_price_currency'", 'to': "orm['common.Currency']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Size']"})
        },
        'carts.size': {
            'Meta': {'object_name': 'Size'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Image']"}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        },
        'carts.sizetranslation': {
            'Meta': {'db_table': "'carts_size_translation'", 'unique_together': "[('language_code', 'master')]", 'object_name': 'SizeTranslation'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'translations'", 'to': "orm['carts.Size']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'carts.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'carrier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Carrier']"}),
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'cart_subscription_criterias'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['common.Criteria']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customers.Customer']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'carrier': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['carts.Carrier']"}),
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'thematic_criterias'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['common.Criteria']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_duration': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '7', 'blank': 'True'}),
            'end_period': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '7', 'blank': 'True'}),
            'frequency': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'max_length': '2', 'blank': 'True'}),
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
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Image']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'receive_only_once': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['carts.Size']"}),
            'start_duration': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '7', 'blank': 'True'}),
            'start_period': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '10', 'blank': 'True'})
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
            'language_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'translations'", 'to': "orm['carts.Thematic']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'common.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['common.Country']"}),
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '30'}),
            'symbol': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'common.image': {
            'Meta': {'object_name': 'Image'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '200'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'customers.customer': {
            'Meta': {'object_name': 'Customer'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['accounts.Account']"}),
            'billing_address': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Address']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_address': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Address']"}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Image']"}),
            'pro': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'relay_address': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Address']"}),
            'shipping_address': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Address']"})
        },
        'products.category': {
            'Meta': {'object_name': 'Category'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'blank': 'True', 'to': "orm['accounts.Author']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'categories_rel_+'", 'blank': 'True', 'to': "orm['products.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Image']"})
        },
        'products.product': {
            'Meta': {'object_name': 'Product'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'+'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['products.Category']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Image']"}),
            'products_parent': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'products_children'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['products.Product']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"})
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
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'product_criterias'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['common.Criteria']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Image']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product_product'", 'to': "orm['products.Product']"}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'product_suppliers'", 'symmetrical': 'False', 'blank': 'True', 'to': "orm['suppliers.Supplier']"}),
            'weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'suppliers.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'delivery_delay': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'blank': 'True', 'to': "orm['common.Image']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'suppliers_rel_+'", 'blank': 'True', 'to': "orm['suppliers.Supplier']"}),
            'threshold_order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['carts']