# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Wallet.rib'
        db.add_column('wallets_wallet', 'rib',
                      self.gf('django.db.models.fields.CharField')(null=True, max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Wallet.payal'
        db.add_column('wallets_wallet', 'payal',
                      self.gf('django.db.models.fields.CharField')(null=True, max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Wallet.bitcoin'
        db.add_column('wallets_wallet', 'bitcoin',
                      self.gf('django.db.models.fields.CharField')(null=True, max_length=200, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Wallet.rib'
        db.delete_column('wallets_wallet', 'rib')

        # Deleting field 'Wallet.payal'
        db.delete_column('wallets_wallet', 'payal')

        # Deleting field 'Wallet.bitcoin'
        db.delete_column('wallets_wallet', 'bitcoin')


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'common.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['common.Country']", 'blank': 'True'}),
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
        'common.currency': {
            'Meta': {'object_name': 'Currency'},
            'exchange_rate': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
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
            'billing_address': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['common.Address']", 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_address': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['common.Address']", 'blank': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['common.Image']", 'blank': 'True'}),
            'shipping_address': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['common.Address']", 'blank': 'True'})
        },
        'wallets.credit': {
            'Meta': {'object_name': 'Credit'},
            'amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Currency']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'c'"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'w'"}),
            'wallet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wallets.Wallet']"})
        },
        'wallets.history': {
            'Meta': {'object_name': 'History'},
            'amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'wallet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wallets.Wallet']"})
        },
        'wallets.wallet': {
            'Meta': {'object_name': 'Wallet'},
            'balance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'bitcoin': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['customers.Customer']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payal': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'rib': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'target_currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Currency']"})
        },
        'wallets.withdraw': {
            'Meta': {'object_name': 'Withdraw'},
            'amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Currency']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'c'"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'w'"}),
            'wallet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wallets.Wallet']"})
        }
    }

    complete_apps = ['wallets']