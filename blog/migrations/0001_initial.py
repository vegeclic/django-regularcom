# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TaggedItem'
        db.create_table('blog_taggeditem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], related_name='blog_tags')),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('blog', ['TaggedItem'])

        # Adding model 'CategoryTranslation'
        db.create_table('blog_category_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Category'], related_name='translations', null=True)),
        ))
        db.send_create_signal('blog', ['CategoryTranslation'])

        # Adding unique constraint on 'CategoryTranslation', fields ['language_code', 'master']
        db.create_unique('blog_category_translation', ['language_code', 'master_id'])

        # Adding model 'Category'
        db.create_table('blog_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('date_last_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
        ))
        db.send_create_signal('blog', ['Category'])

        # Adding model 'ArticleTranslation'
        db.create_table('blog_article_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Article'], related_name='translations', null=True)),
        ))
        db.send_create_signal('blog', ['ArticleTranslation'])

        # Adding unique constraint on 'ArticleTranslation', fields ['language_code', 'master']
        db.create_unique('blog_article_translation', ['language_code', 'master_id'])

        # Adding model 'Article'
        db.create_table('blog_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('date_last_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
            ('main_image', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, to=orm['common.Image'], related_name='blog_article_main_image', unique=True, null=True)),
            ('title_image', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, to=orm['common.Image'], related_name='blog_article_title_image', unique=True, null=True)),
            ('thumb_image', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, to=orm['common.Image'], related_name='blog_article_thumb_image', unique=True, null=True)),
        ))
        db.send_create_signal('blog', ['Article'])

        # Adding M2M table for field authors on 'Article'
        m2m_table_name = db.shorten_name('blog_article_authors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['blog.article'], null=False)),
            ('author', models.ForeignKey(orm['accounts.author'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'author_id'])

        # Adding M2M table for field categories on 'Article'
        m2m_table_name = db.shorten_name('blog_article_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['blog.article'], null=False)),
            ('category', models.ForeignKey(orm['blog.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'category_id'])

        # Adding model 'Comment'
        db.create_table('blog_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['accounts.Account'], null=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Article'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('date_last_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
        ))
        db.send_create_signal('blog', ['Comment'])


    def backwards(self, orm):
        # Removing unique constraint on 'ArticleTranslation', fields ['language_code', 'master']
        db.delete_unique('blog_article_translation', ['language_code', 'master_id'])

        # Removing unique constraint on 'CategoryTranslation', fields ['language_code', 'master']
        db.delete_unique('blog_category_translation', ['language_code', 'master_id'])

        # Deleting model 'TaggedItem'
        db.delete_table('blog_taggeditem')

        # Deleting model 'CategoryTranslation'
        db.delete_table('blog_category_translation')

        # Deleting model 'Category'
        db.delete_table('blog_category')

        # Deleting model 'ArticleTranslation'
        db.delete_table('blog_article_translation')

        # Deleting model 'Article'
        db.delete_table('blog_article')

        # Removing M2M table for field authors on 'Article'
        db.delete_table(db.shorten_name('blog_article_authors'))

        # Removing M2M table for field categories on 'Article'
        db.delete_table(db.shorten_name('blog_article_categories'))

        # Deleting model 'Comment'
        db.delete_table('blog_comment')


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
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
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['common.Image']", 'related_name': "'+'", 'unique': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'})
        },
        'blog.article': {
            'Meta': {'object_name': 'Article'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['accounts.Author']", 'symmetrical': 'False', 'related_name': "'blog_article_authors'"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['blog.Category']", 'symmetrical': 'False', 'related_name': "'blog_article_categories'", 'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['common.Image']", 'related_name': "'blog_article_main_image'", 'unique': 'True', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'thumb_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['common.Image']", 'related_name': "'blog_article_thumb_image'", 'unique': 'True', 'null': 'True'}),
            'title_image': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'to': "orm['common.Image']", 'related_name': "'blog_article_title_image'", 'unique': 'True', 'null': 'True'})
        },
        'blog.articletranslation': {
            'Meta': {'object_name': 'ArticleTranslation', 'unique_together': "[('language_code', 'master')]", 'db_table': "'blog_article_translation'"},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Article']", 'related_name': "'translations'", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'blog.category': {
            'Meta': {'object_name': 'Category'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'blog.categorytranslation': {
            'Meta': {'object_name': 'CategoryTranslation', 'unique_together': "[('language_code', 'master')]", 'db_table': "'blog_category_translation'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Category']", 'related_name': "'translations'", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['blog']