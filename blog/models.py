#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# Authors:
# Caner Candan <caner@candan.fr>, http://caner.candan.fr
# Geraldine Starke <geraldine@starke.fr>, http://www.vegeclic.fr
#

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class TaggedItem(models.Model):
    tag = models.SlugField(_('tag'))
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'), related_name='blog_tags')
    object_id = models.PositiveIntegerField(_('object id'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self): return self.tag

class Category(models.Model):
    class Meta:
        verbose_name_plural = _('categories')

    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return self.name

class Article(models.Model):
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(max_length=200)
    body = models.TextField(_('body'))
    authors = models.ManyToManyField('accounts.Author', related_name='blog_article_authors', verbose_name=_('authors'))
    tags = generic.GenericRelation(TaggedItem, verbose_name=_('tags'), related_name='blog_article_tags')
    categories = models.ManyToManyField(Category, null=True, blank=True, related_name='blog_article_categories', verbose_name=_('categories'))
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='blog_article_main_image', verbose_name=_('main image'))
    title_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='blog_article_title_image', verbose_name=_('title image'))
    thumb_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='blog_article_thumb_image', verbose_name=_('thumb image'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
    period_start = models.DateField(_('period start'), null=True, blank=True)
    period_end = models.DateField(_('period end'), null=True, blank=True)
    date_last_blogging_sent = models.DateTimeField(_('date last blogging sent'), null=True, blank=True)
    enabled = models.BooleanField(_('enabled'), default=True)

    def __unicode__(self): return self.title.title()

class Comment(models.Model):
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('participant'), null=True, blank=True)
    article = models.ForeignKey(Article, verbose_name=_('article'))
    body = models.TextField(_('body'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

class Microblog(models.Model):
    article = models.ForeignKey(Article, verbose_name=_('article'))
    message = models.CharField(_('message'), max_length=140)
    date_last_sent = models.DateTimeField(_('date last sent'), null=True, blank=True)

class Reader(models.Model):
    account = models.OneToOneField(settings.AUTH_USER_MODEL)
    articles_read = models.ManyToManyField(Article, null=True, blank=True, related_name='blog_reader_articles_read', verbose_name=_('articles_read'))

    def __unicode__(self): return self.account
