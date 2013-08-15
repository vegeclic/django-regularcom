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

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.models import inlineformset_factory
import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week
import common.models as cm

class StatusBasedModel(models.Model):
    STATUS_CHOICES = (
        ('d', _('Draft')),
        ('p', _('Published')),
        ('e', _('Expired')),
        ('w', _('Withdrawn')),
    )
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='d')

class Thematic(StatusBasedModel):
    name = models.CharField(_('name'), max_length=100, unique=True)
    products = models.ManyToManyField('products.Product', null=True, blank=True, related_name='thematic_products', verbose_name=_('products'))
    criterias = models.ManyToManyField('common.Criteria', null=True, blank=True, related_name='thematic_criterias', verbose_name=_('criterias'))
    start_period = models.DateField(_('start period'), null=True, blank=True, default=datetime.date.today)
    end_period = models.DateField(_('end period'), null=True, blank=True)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+', verbose_name=_('main image'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

class Size(StatusBasedModel):
    name = models.CharField(max_length=100, unique=True)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+', verbose_name=_('main image'))

    def __unicode__(self):
        try:
            selected_price = self.price_set.get(currency=cm.Parameter.objects.get(name='default currency').content_object)
        except ObjectDoesNotExist:
            selected_price = None
        return '%s%s' % (self.name, (' (%s)' % selected_price.__unicode__()) if selected_price else "")

class Price(models.Model):
    class Meta:
        unique_together = ('size', 'currency')

    size = models.ForeignKey(Size, verbose_name=_('size'))
    currency = models.ForeignKey('common.Currency', related_name='cart_size_price_currency', verbose_name=_('currency'))
    price = models.FloatField(_('price'))

    def __unicode__(self): return ('%s %s' % (self.price, self.currency.symbol)).strip()

__weeks = []
for y in range(settings.START_YEAR, Week.thisweek().year+2): __weeks += Week.weeks_of_year(y)
WEEKS_CHOICES = [(str(w), str(w)) for w in __weeks]

class Delivery(models.Model):
    class Meta:
        verbose_name_plural = _('deliveries')

    subscription = models.ForeignKey('Subscription', verbose_name=_('subscription'))
    date = models.CharField(_('date'), max_length=7, choices=WEEKS_CHOICES)
    STATUS_CHOICES = (
        ('d', _('Draft')),
        ('v', _('Validated')),
        ('D', _('Delivered')),
        ('e', _('Expired')),
        ('w', _('Withdrawn')),
    )
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='d')
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return self.date

class ContentProduct(models.Model):
    class Meta:
        unique_together = ('content', 'product')

    content = models.ForeignKey('Content', verbose_name=_('content'))
    product = models.ForeignKey('suppliers.Product', verbose_name=_('product'))
    quantity = models.PositiveIntegerField(_('quantity'), default=1)

class Content(models.Model):
    class Meta:
        unique_together = ('delivery', 'extent')

    delivery = models.ForeignKey('Delivery', verbose_name=_('delivery'))
    extent = models.ForeignKey('Extent', verbose_name=_('extent'))

    def __unicode__(self): return '%s, %s' % (self.delivery, self.extent)

class Subscription(models.Model):
    customer = models.ForeignKey('customers.Customer', verbose_name=_('customer'))
    size = models.ForeignKey(Size, verbose_name=_('size'))
    FREQUENCY_CHOICES = (
        (1, _('Once a week')),
        (2, _('Every two weeks')),
        (3, _('Every three weeks')),
        (4, _('Once a month')),
        (8, _('Every two months')),
        (13, _('Once a quarter')),
        (26, _('Every 6 months')),
    )
    frequency = models.PositiveIntegerField(_('frequency'), max_length=2, choices=FREQUENCY_CHOICES, default=2, help_text=_('Delivery made sure Tuesday'))
    start = models.CharField(_('start'), max_length=7, choices=WEEKS_CHOICES,
                             help_text=_('Here is the beginnig week of the subscription.'))
    end = models.CharField(_('end'), max_length=7, choices=WEEKS_CHOICES,
                           help_text=_('Here is the ending week of the subscription.'))
    criterias = models.ManyToManyField('common.Criteria', null=True, blank=True, related_name='cart_subscription_criterias', verbose_name=_('criterias'))
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    STATUS_CHOICES = (
        ('d', _('Draft')),
        ('v', _('Validated')),
        ('e', _('Expired')),
        ('w', _('Withdrawn')),
    )
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='d')
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return '%s, %s, %s, %s, %s' % (self.customer.__unicode__(), self.size.name, self.get_frequency_display(), self.get_start_display(), self.get_end_display())

    def save(self, *args, **kwargs):
        super(Subscription, self).save(*args, **kwargs)
        if self.status == 'v':
            s, e = Week.fromstring(self.start), Week.fromstring(self.end)
            for i in range(0, e+1-s, self.frequency):
                d = self.delivery_set.create(date=s+i)
                for extent in self.extent_set.filter(subscription=self):
                    d.content_set.create(extent=extent)

class Extent(models.Model):
    class Meta:
        unique_together = ('subscription', 'product')

    subscription = models.ForeignKey(Subscription, verbose_name=_('subscription'))
    product = models.ForeignKey('products.Product', verbose_name=_('product'))
    extent = models.PositiveSmallIntegerField(_('extent'))

    def __unicode__(self): return '%s, %s, %s' % (self.subscription.__unicode__(), self.product.__unicode__(), self.extent)
