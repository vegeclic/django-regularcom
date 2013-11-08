# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ProductTranslation', fields ['slug']
        db.delete_unique('products_product_translation', ['slug'])

        # Removing unique constraint on 'CategoryTranslation', fields ['slug']
        db.delete_unique('products_category_translation', ['slug'])


        # Changing field 'CategoryTranslation.slug'
        db.alter_column('products_category_translation', 'slug', self.gf('django.db.models.fields.SlugField')(null=True, max_length=50))

        # Changing field 'ProductTranslation.slug'
        db.alter_column('products_product_translation', 'slug', self.gf('django.db.models.fields.SlugField')(null=True, max_length=50))

    def backwards(self, orm):

        # Changing field 'CategoryTranslation.slug'
        db.alter_column('products_category_translation', 'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, default=''))
        # Adding unique constraint on 'CategoryTranslation', fields ['slug']
        db.create_unique('products_category_translation', ['slug'])


        # Changing field 'ProductTranslation.slug'
        db.alter_column('products_product_translation', 'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, default=''))
        # Adding unique constraint on 'ProductTranslation', fields ['slug']
        db.create_unique('products_product_translation', ['slug'])


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
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['common.Image']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
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
        'products.category': {
            'Meta': {'object_name': 'Category'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'symmetrical': 'False', 'to': "orm['accounts.Author']", 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'categories_rel_+'", 'to': "orm['products.Category']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['common.Image']", 'blank': 'True'})
        },
        'products.categorytranslation': {
            'Meta': {'db_table': "'products_category_translation'", 'unique_together': "[('language_code', 'master')]", 'object_name': 'CategoryTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'translations'", 'to': "orm['products.Category']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'null': 'True', 'max_length': '50', 'blank': 'True'})
        },
        'products.product': {
            'Meta': {'object_name': 'Product'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'+'", 'symmetrical': 'False', 'to': "orm['products.Category']", 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'related_name': "'+'", 'to': "orm['common.Image']", 'blank': 'True'}),
            'products_parent': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'products_children'", 'symmetrical': 'False', 'to': "orm['products.Product']", 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'d'"})
        },
        'products.producttranslation': {
            'Meta': {'db_table': "'products_product_translation'", 'unique_together': "[('language_code', 'master')]", 'object_name': 'ProductTranslation'},
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'translations'", 'to': "orm['products.Product']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'null': 'True', 'max_length': '50', 'blank': 'True'})
        },
        'products.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tag': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['products']