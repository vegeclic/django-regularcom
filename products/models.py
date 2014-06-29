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
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class TaggedItem(models.Model):
    tag = models.SlugField(_('tag'))
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(_('object id'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self): return self.tag

class Category(models.Model):
    class Meta:
        verbose_name_plural = _('categories')

    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), null=True, blank=True)
    categories = models.ManyToManyField('self', null=True, blank=True, related_name='+', verbose_name=_('categories'))
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+', verbose_name=_('main image'))
    tags = generic.GenericRelation(TaggedItem, verbose_name=_('tags'))
    authors = models.ManyToManyField('accounts.Author', null=True, blank=True, verbose_name=_('authors'))

    def __unicode__(self): return self.name

class Product(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), null=True, blank=True)
    body = models.TextField(_('body'), blank=True)
    STATUS_CHOICES = (
        ('d', _('Draft')),
        ('p', _('Published')),
        ('e', _('Expired')),
        ('w', _('Withdrawn')),
    )
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='d')
    categories = models.ManyToManyField(Category, null=True, blank=True, related_name='+', verbose_name=_('categories'))
    products_parent = models.ManyToManyField('self', symmetrical=False, null=True, blank=True, related_name='products_children', verbose_name=_('products parent'))
    tags = generic.GenericRelation(TaggedItem, verbose_name=_('tags'))
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+', verbose_name=_('main image'))
    tax = models.ForeignKey('common.Tax', related_name='product_price_tax', verbose_name=_('tax'), null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return self.name

    def get_absolute_url(self):
        return reverse_lazy('catalog_product_id_slug', args=[self.id, self.slug])
