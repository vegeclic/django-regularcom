# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Article.summary'
        db.add_column('blog_article', 'summary',
                      self.gf('django.db.models.fields.TextField')(blank=True, null=True),
                      keep_default=False)

        # Adding field 'Article.linebreaks'
        db.add_column('blog_article', 'linebreaks',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Article.summary'
        db.delete_column('blog_article', 'summary')

        # Deleting field 'Article.linebreaks'
        db.delete_column('blog_article', 'linebreaks')


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
            'newsletter': ('django.db.models.fields.CharField', [], {'default': "'w'", 'max_length': '1'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'accounts.author': {
            'Meta': {'object_name': 'Author'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.Account']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'related_name': "'+'", 'unique': 'True'}),
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
            'date_last_blogging_sent': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linebreaks': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'related_name': "'blog_article_main_image'", 'unique': 'True'}),
            'period_end': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'period_start': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'slug_de': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'slug_fr': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'thumb_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'related_name': "'blog_article_thumb_image'", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_de': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'title_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'null': 'True', 'to': "orm['common.Image']", 'related_name': "'blog_article_title_image'", 'unique': 'True'})
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
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['accounts.Account']", 'null': 'True'})
        },
        'blog.microblog': {
            'Meta': {'object_name': 'Microblog'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Article']"}),
            'date_last_sent': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'message_de': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '140'}),
            'message_fr': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '140'})
        },
        'blog.reader': {
            'Meta': {'object_name': 'Reader'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.Account']", 'unique': 'True'}),
            'articles_read': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'to': "orm['blog.Article']", 'symmetrical': 'False', 'related_name': "'blog_reader_articles_read'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['blog']