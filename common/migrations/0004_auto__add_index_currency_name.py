# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Currency', fields ['name']
        db.create_index('common_currency', ['name'])


    def backwards(self, orm):
        # Removing index on 'Currency', fields ['name']
        db.delete_index('common_currency', ['name'])


    models = {
        'common.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['common.Country']", 'null': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'common.criteriatranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'CriteriaTranslation', 'db_table': "'common_criteria_translation'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Criteria']", 'related_name': "'translations'", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'})
        },
        'common.currency': {
            'Meta': {'object_name': 'Currency'},
            'exchange_rate': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True', 'unique': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'common.image': {
            'Meta': {'object_name': 'Image'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '200'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'common.parameter': {
            'Meta': {'unique_together': "(('site', 'name'),)", 'object_name': 'Parameter'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['common']