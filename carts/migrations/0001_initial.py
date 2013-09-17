# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Thematic'
        db.create_table('carts_thematic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1, default='d')),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('start_period', self.gf('django.db.models.fields.DateField')(blank=True, null=True, default=datetime.date.today)),
            ('end_period', self.gf('django.db.models.fields.DateField')(blank=True, null=True)),
            ('main_image', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, null=True, to=orm['common.Image'], unique=True, related_name='+')),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('date_last_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
        ))
        db.send_create_signal('carts', ['Thematic'])

        # Adding M2M table for field products on 'Thematic'
        m2m_table_name = db.shorten_name('carts_thematic_products')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('thematic', models.ForeignKey(orm['carts.thematic'], null=False)),
            ('product', models.ForeignKey(orm['products.product'], null=False))
        ))
        db.create_unique(m2m_table_name, ['thematic_id', 'product_id'])

        # Adding M2M table for field criterias on 'Thematic'
        m2m_table_name = db.shorten_name('carts_thematic_criterias')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('thematic', models.ForeignKey(orm['carts.thematic'], null=False)),
            ('criteria', models.ForeignKey(orm['common.criteria'], null=False))
        ))
        db.create_unique(m2m_table_name, ['thematic_id', 'criteria_id'])

        # Adding model 'Size'
        db.create_table('carts_size', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1, default='d')),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('main_image', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, null=True, to=orm['common.Image'], unique=True, related_name='+')),
        ))
        db.send_create_signal('carts', ['Size'])

        # Adding model 'Price'
        db.create_table('carts_price', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['carts.Size'])),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Currency'], related_name='cart_size_price_currency')),
            ('price', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('carts', ['Price'])

        # Adding unique constraint on 'Price', fields ['size', 'currency']
        db.create_unique('carts_price', ['size_id', 'currency_id'])

        # Adding model 'Delivery'
        db.create_table('carts_delivery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['carts.Subscription'])),
            ('date', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1, default='d')),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('date_last_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
        ))
        db.send_create_signal('carts', ['Delivery'])

        # Adding model 'ContentProduct'
        db.create_table('carts_contentproduct', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['carts.Content'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['suppliers.Product'])),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('carts', ['ContentProduct'])

        # Adding unique constraint on 'ContentProduct', fields ['content', 'product']
        db.create_unique('carts_contentproduct', ['content_id', 'product_id'])

        # Adding model 'Content'
        db.create_table('carts_content', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('delivery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['carts.Delivery'])),
            ('extent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['carts.Extent'])),
        ))
        db.send_create_signal('carts', ['Content'])

        # Adding unique constraint on 'Content', fields ['delivery', 'extent']
        db.create_unique('carts_content', ['delivery_id', 'extent_id'])

        # Adding model 'Subscription'
        db.create_table('carts_subscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customers.Customer'])),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['carts.Size'])),
            ('frequency', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=2, default=2)),
            ('start', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('end', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1, default='d')),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('date_last_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
        ))
        db.send_create_signal('carts', ['Subscription'])

        # Adding M2M table for field criterias on 'Subscription'
        m2m_table_name = db.shorten_name('carts_subscription_criterias')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subscription', models.ForeignKey(orm['carts.subscription'], null=False)),
            ('criteria', models.ForeignKey(orm['common.criteria'], null=False))
        ))
        db.create_unique(m2m_table_name, ['subscription_id', 'criteria_id'])

        # Adding model 'Extent'
        db.create_table('carts_extent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['carts.Subscription'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Product'])),
            ('extent', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('carts', ['Extent'])

        # Adding unique constraint on 'Extent', fields ['subscription', 'product']
        db.create_unique('carts_extent', ['subscription_id', 'product_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Extent', fields ['subscription', 'product']
        db.delete_unique('carts_extent', ['subscription_id', 'product_id'])

        # Removing unique constraint on 'Content', fields ['delivery', 'extent']
        db.delete_unique('carts_content', ['delivery_id', 'extent_id'])

        # Removing unique constraint on 'ContentProduct', fields ['content', 'product']
        db.delete_unique('carts_contentproduct', ['content_id', 'product_id'])

        # Removing unique constraint on 'Price', fields ['size', 'currency']
        db.delete_unique('carts_price', ['size_id', 'currency_id'])

        # Deleting model 'Thematic'
        db.delete_table('carts_thematic')

        # Removing M2M table for field products on 'Thematic'
        db.delete_table(db.shorten_name('carts_thematic_products'))

        # Removing M2M table for field criterias on 'Thematic'
        db.delete_table(db.shorten_name('carts_thematic_criterias'))

        # Deleting model 'Size'
        db.delete_table('carts_size')

        # Deleting model 'Price'
        db.delete_table('carts_price')

        # Deleting model 'Delivery'
        db.delete_table('carts_delivery')

        # Deleting model 'ContentProduct'
        db.delete_table('carts_contentproduct')

        # Deleting model 'Content'
        db.delete_table('carts_content')

        # Deleting model 'Subscription'
        db.delete_table('carts_subscription')

        # Removing M2M table for field criterias on 'Subscription'
        db.delete_table(db.shorten_name('carts_subscription_criterias'))

        # Deleting model 'Extent'
        db.delete_table('carts_extent')


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
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
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'})
        },
        'carts.content': {
            'Meta': {'object_name': 'Content', 'unique_together': "(('delivery', 'extent'),)"},
            'delivery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Delivery']"}),
            'extent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Extent']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Subscription']"})
        },
        'carts.extent': {
            'Meta': {'object_name': 'Extent', 'unique_together': "(('subscription', 'product'),)"},
            'extent': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Subscription']"})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"})
        },
        'carts.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Criteria']", 'related_name': "'cart_subscription_criterias'", 'symmetrical': 'False'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customers.Customer']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'end': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'frequency': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '2', 'default': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['carts.Size']"}),
            'start': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"})
        },
        'carts.thematic': {
            'Meta': {'object_name': 'Thematic'},
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Criteria']", 'related_name': "'thematic_criterias'", 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'end_period': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'to': "orm['products.Product']", 'related_name': "'thematic_products'", 'symmetrical': 'False'}),
            'start_period': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True', 'default': 'datetime.date.today'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"})
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
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'customers.customer': {
            'Meta': {'object_name': 'Customer'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.Account']", 'unique': 'True'}),
            'billing_address': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Address']", 'unique': 'True', 'related_name': "'+'"}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_address': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Address']", 'unique': 'True', 'related_name': "'+'"}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'related_name': "'+'"}),
            'shipping_address': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Address']", 'unique': 'True', 'related_name': "'+'"})
        },
        'products.category': {
            'Meta': {'object_name': 'Category'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'to': "orm['accounts.Author']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'related_name': "'+'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'products.product': {
            'Meta': {'object_name': 'Product'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'to': "orm['products.Category']", 'related_name': "'+'", 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'related_name': "'+'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
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
            'criterias': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Criteria']", 'related_name': "'product_criterias'", 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'related_name': "'+'"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']", 'related_name': "'+'"}),
            'sku': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'to': "orm['suppliers.Supplier']", 'related_name': "'product_suppliers'", 'symmetrical': 'False'}),
            'weight': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'})
        },
        'suppliers.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'delivery_delay': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'related_name': "'+'"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'to': "orm['suppliers.Supplier']", 'related_name': "'suppliers_rel_+'"}),
            'threshold_order': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['carts']