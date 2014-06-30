# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.utils.text import slugify

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Article.slug_de'
        db.add_column('blog_article', 'slug_de',
                      self.gf('django.db.models.fields.SlugField')(blank=True, null=True, max_length=200),
                      keep_default=False)

        # Adding field 'Article.slug_fr'
        db.add_column('blog_article', 'slug_fr',
                      self.gf('django.db.models.fields.SlugField')(blank=True, null=True, max_length=200),
                      keep_default=False)

        if not db.dry_run:
            for a in orm.Article.objects.all():
                if a.title_de: a.slug_de = slugify(a.title_de)
                if a.title_fr: a.slug_fr = slugify(a.title_fr)
                a.save()

        # Adding field 'Category.slug'
        db.add_column('blog_category', 'slug',
                      self.gf('django.db.models.fields.SlugField')(max_length=200, default=''),
                      keep_default=False)

        # Adding field 'Category.slug_de'
        db.add_column('blog_category', 'slug_de',
                      self.gf('django.db.models.fields.SlugField')(blank=True, null=True, max_length=200),
                      keep_default=False)

        # Adding field 'Category.slug_fr'
        db.add_column('blog_category', 'slug_fr',
                      self.gf('django.db.models.fields.SlugField')(blank=True, null=True, max_length=200),
                      keep_default=False)

        if not db.dry_run:
            for c in orm.Category.objects.all():
                if c.name_de: c.slug_de = slugify(c.name_de)
                if c.name_fr: c.slug_fr = slugify(c.name_fr)
                c.save()

    def backwards(self, orm):
        # Deleting field 'Article.slug_de'
        db.delete_column('blog_article', 'slug_de')

        # Deleting field 'Article.slug_fr'
        db.delete_column('blog_article', 'slug_fr')

        # Deleting field 'Category.slug'
        db.delete_column('blog_category', 'slug')

        # Deleting field 'Category.slug_de'
        db.delete_column('blog_category', 'slug_de')

        # Deleting field 'Category.slug_fr'
        db.delete_column('blog_category', 'slug_fr')


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '255'}),
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
        'blog.article': {
            'Meta': {'object_name': 'Article'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['accounts.Author']", 'symmetrical': 'False', 'related_name': "'blog_article_authors'"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'body_de': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'body_fr': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'to': "orm['blog.Category']", 'symmetrical': 'False', 'related_name': "'blog_article_categories'"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'related_name': "'blog_article_main_image'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'slug_de': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'slug_fr': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'thumb_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'related_name': "'blog_article_thumb_image'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_de': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'title_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'unique': 'True', 'related_name': "'blog_article_title_image'"})
        },
        'blog.category': {
            'Meta': {'object_name': 'Category'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name_de': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'slug_de': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'slug_fr': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'})
        },
        'blog.comment': {
            'Meta': {'object_name': 'Comment'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Article']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['accounts.Account']"})
        },
        'blog.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'blog_tags'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'tag': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
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
        }
    }

    complete_apps = ['blog']
