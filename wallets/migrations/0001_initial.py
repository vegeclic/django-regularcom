# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Wallet'
        db.create_table('wallets_wallet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['customers.Customer'], unique=True)),
            ('balance', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('target_currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Currency'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('date_last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('wallets', ['Wallet'])

        # Adding model 'History'
        db.create_table('wallets_history', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wallet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wallets.Wallet'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('amount', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('date_last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('wallets', ['History'])

        # Adding model 'Credit'
        db.create_table('wallets_credit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wallet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wallets.Wallet'])),
            ('payment_type', self.gf('django.db.models.fields.CharField')(default='c', max_length=1)),
            ('amount', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Currency'])),
            ('payment_date', self.gf('django.db.models.fields.DateField')(blank=True, null=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('date_last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='d', max_length=1)),
        ))
        db.send_create_signal('wallets', ['Credit'])


    def backwards(self, orm):
        # Deleting model 'Wallet'
        db.delete_table('wallets_wallet')

        # Deleting model 'History'
        db.delete_table('wallets_history')

        # Deleting model 'Credit'
        db.delete_table('wallets_credit')


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
            'Meta': {'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'customers.customer': {
            'Meta': {'object_name': 'Customer'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.Account']", 'unique': 'True'}),
            'billing_address': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['common.Address']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_address': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['common.Address']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['common.Image']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'}),
            'shipping_address': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['common.Address']", 'blank': 'True', 'related_name': "'+'", 'null': 'True'})
        },
        'wallets.credit': {
            'Meta': {'object_name': 'Credit'},
            'amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Currency']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_date': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'default': "'c'", 'max_length': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'d'", 'max_length': '1'}),
            'wallet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wallets.Wallet']"})
        },
        'wallets.history': {
            'Meta': {'object_name': 'History'},
            'amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'wallet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wallets.Wallet']"})
        },
        'wallets.wallet': {
            'Meta': {'object_name': 'Wallet'},
            'balance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'customer': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['customers.Customer']", 'unique': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target_currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Currency']"})
        }
    }

    complete_apps = ['wallets']