# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Microblog'
        db.create_table('blog_microblog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Article'])),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('message_de', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True, null=True)),
            ('message_fr', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True, null=True)),
            ('date_last_sent', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('blog', ['Microblog'])

        # Adding field 'Article.newsletter_sent'
        db.add_column('blog_article', 'newsletter_sent',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Article.date_last_blogging_sent'
        db.add_column('blog_article', 'date_last_blogging_sent',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Microblog'
        db.delete_table('blog_microblog')

        # Deleting field 'Article.newsletter_sent'
        db.delete_column('blog_article', 'newsletter_sent')

        # Deleting field 'Article.date_last_blogging_sent'
        db.delete_column('blog_article', 'date_last_blogging_sent')


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'blank': 'True', 'related_name': "'+'", 'to': "orm['common.Image']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        'blog.article': {
            'Meta': {'object_name': 'Article'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['accounts.Author']", 'related_name': "'blog_article_authors'", 'symmetrical': 'False'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'body_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'to': "orm['blog.Category']", 'blank': 'True', 'related_name': "'blog_article_categories'", 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_blogging_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'blank': 'True', 'related_name': "'blog_article_main_image'", 'to': "orm['common.Image']"}),
            'newsletter_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'slug_de': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'slug_fr': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'thumb_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'blank': 'True', 'related_name': "'blog_article_thumb_image'", 'to': "orm['common.Image']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_de': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'title_image': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'blank': 'True', 'related_name': "'blog_article_title_image'", 'to': "orm['common.Image']"})
        },
        'blog.category': {
            'Meta': {'object_name': 'Category'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'slug_de': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'slug_fr': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'})
        },
        'blog.comment': {
            'Meta': {'object_name': 'Comment'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Article']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['accounts.Account']"})
        },
        'blog.microblog': {
            'Meta': {'object_name': 'Microblog'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Article']"}),
            'date_last_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'message_de': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True', 'null': 'True'}),
            'message_fr': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True', 'null': 'True'})
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
            'Meta': {'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['blog']