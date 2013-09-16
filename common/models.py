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
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class Image(models.Model):
    def image_name(self, filename):
        package = self.content_object.__module__.split('.')[0].lower()
        module = self.content_object.__class__.__name__.lower()
        slug = self.content_object.slug if 'slug' in dir(self.content_object) else str(self.object_id)
        return '/'.join([package, module, slug, filename])

    image = models.ImageField(upload_to=image_name, max_length=200)
    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self): return self.image

class Country(models.Model):
    class Meta:
        verbose_name_plural = 'Countries'

    name = models.CharField(max_length=30, unique=True)

    def __unicode__(self): return self.name

class Address(models.Model):
    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )
    gender = models.CharField(_('gender'), choices=GENDER_CHOICES, max_length=1, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    street = models.CharField(_('street'), max_length=100, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=100, blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True, verbose_name=_('country'))
    home_phone = models.CharField(_('home phone'), max_length=100, blank=True)
    mobile_phone = models.CharField(_('mobile phone'), max_length=100, blank=True)
    email = models.EmailField(_('email'), blank=True)

    def __unicode__(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

class Currency(models.Model):
    class Meta:
        verbose_name_plural = _("currencies")

    name = models.CharField(_('name'), max_length=30, unique=True)
    symbol = models.CharField(_('symbol'), max_length=30, unique=True)
    exchange_rate = models.FloatField(_('exchange rate'), default=1)

    def __unicode__(self): return ('%s (%s)' % (self.name, self.symbol)).strip()

class Criteria(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)

    def __unicode__(self): return self.name

class Parameter(models.Model):
    class Meta:
        unique_together = ('site', 'name')

    site = models.ForeignKey('sites.Site', verbose_name=_('site'))
    name = models.CharField(_('name'), max_length=100, unique=True)
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(_('object id'), default=0)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self): return '%s %s' % (self.site, self.name)
