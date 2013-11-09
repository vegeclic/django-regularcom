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
from hvad.models import TranslatableModel, TranslatedFields

class TaggedItem(models.Model):
    tag = models.SlugField(_('tag'))
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'), related_name='blog_tags')
    object_id = models.PositiveIntegerField(_('object id'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self): return self.tag

class Category(TranslatableModel):
    class Meta:
        verbose_name_plural = _('categories')

    translations = TranslatedFields(
        name = models.CharField(_('name'), max_length=200)
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return self.lazy_translation_getter('name', 'Category: %s' % self.pk)

class Article(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(_('title'), max_length=200),
        body = models.TextField(_('body')),
    )
    authors = models.ManyToManyField('accounts.Author', related_name='blog_article_authors', verbose_name=_('authors'))
    slug = models.SlugField(max_length=200)
    enabled = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='blog_article_main_image', verbose_name=_('main image'))
    title_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='blog_article_title_image', verbose_name=_('title image'))
    thumb_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='blog_article_thumb_image', verbose_name=_('thumb image'))
    tags = generic.GenericRelation(TaggedItem, verbose_name=_('tags'), related_name='blog_article_tags')
    categories = models.ManyToManyField(Category, null=True, blank=True, related_name='blog_article_categories', verbose_name=_('categories'))

class Comment(models.Model):
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('participant'), null=True, blank=True)
    article = models.ForeignKey(Article, verbose_name=_('article'))
    body = models.TextField(_('body'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
