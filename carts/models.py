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
from hvad.models import TranslatableModel, TranslatedFields
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.models import inlineformset_factory
from django.contrib import messages
import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week
import common.models as cm
import wallets.models as wm

FREQUENCY_CHOICES = (
    (1, _('Once a week')),
    (2, _('Every two weeks')),
    (3, _('Every three weeks')),
    (4, _('Once a month')),
    (8, _('Every two months')),
    (13, _('Once a quarter')),
    (26, _('Every 6 months')),
)

FREQUENCY_DEFAULT = 2

__weeks = []
for y in range(settings.START_YEAR, Week.thisweek().year+2): __weeks += Week.weeks_of_year(y)
WEEKS_CHOICES = [(str(w), str(w)) for w in __weeks]

class Thematic(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_('name'), max_length=100, unique=True),
        body = models.TextField(_('body'), blank=True),
    )
    size = models.ForeignKey('Size', verbose_name=_('size'), null=True, blank=True)
    frequency = models.PositiveIntegerField(_('frequency'), max_length=2, choices=FREQUENCY_CHOICES, default=FREQUENCY_DEFAULT, help_text=_('Delivery made sure Tuesday'), null=True, blank=True)
    start_duration = models.CharField(_('start duration'), max_length=7, choices=WEEKS_CHOICES,
                                      help_text=_('Here is the beginnig week of the duration.'),
                                      null=True, blank=True)
    end_duration = models.CharField(_('end duration'), max_length=7, choices=WEEKS_CHOICES,
                                    help_text=_('Here is the ending week of the duration.'),
                                    null=True, blank=True)
    criterias = models.ManyToManyField('common.Criteria', null=True, blank=True, related_name='thematic_criterias', verbose_name=_('criterias'))
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    start_period = models.CharField(_('start period'), max_length=10, choices=WEEKS_CHOICES,
                                    help_text=_('Here is the beginnig week of the period.'),
                                    null=True, blank=True)
    end_period = models.CharField(_('end period'), max_length=7, choices=WEEKS_CHOICES,
                                  help_text=_('Here is the ending week of the period.'),
                                  null=True, blank=True)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+', verbose_name=_('main image'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(_('enabled'), default=False)

    def __unicode__(self): return self.lazy_translation_getter('name', 'Thematic: %s' % self.pk)

class Size(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_('name'), max_length=100, unique=True),
        body = models.TextField(_('body'), blank=True),
    )
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+', verbose_name=_('main image'))
    enabled = models.BooleanField(_('enabled'), default=False)

    def default_price(self):
        try:
            return self.price_set.get(currency=cm.Parameter.objects.get(name='default currency').content_object)
        except Size.DoesNotExist:
            return None

    def __unicode__(self):
        price = self.default_price()
        return '%s%s' % (self.lazy_translation_getter('name', 'Size: %s' % self.pk),
                         (' (%s)' % price.__unicode__()) if price else "")

class Price(models.Model):
    class Meta:
        unique_together = ('size', 'currency')

    size = models.ForeignKey(Size, verbose_name=_('size'))
    currency = models.ForeignKey('common.Currency', related_name='cart_size_price_currency', verbose_name=_('currency'))
    price = models.FloatField(_('price'))

    def __unicode__(self): return ('%s %s' % (self.price, self.currency.symbol)).strip()

class Delivery(models.Model):
    class Meta:
        verbose_name_plural = _('deliveries')

    subscription = models.ForeignKey('Subscription', verbose_name=_('subscription'))
    date = models.CharField(_('date'), max_length=7, choices=WEEKS_CHOICES)
    STATUS_CHOICES = (
        ('w', _('In waiting')),
        ('p', _('Payed')),
        ('P', _('In progress')),
        ('d', _('Delivered')),
        ('c', _('Canceled')),
        ('e', _('Expired')),
    )
    SUCCESS_CHOICES = ['p', 'P', 'd']
    FAILED_CHOICES = ['c', 'e']
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='w')
    payed_price = models.FloatField(_('payed price'), null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return '%s - %s' % (self.subscription.__unicode__(), self.date)

    def save(self, *args, **kwargs):
        if self.status == 'p':
            wallet = wm.Wallet.objects.get(customer__account=self.subscription.customer)
            amount = self.payed_price
            if wallet.balance < amount:
                raise ValueError(_('You dont have enough money in your wallet to buy it.'))
            wallet.balance -= amount
            wallet.save()
            h = wm.History(wallet=wallet, content_type=ContentType.objects.get(model='delivery'),
                           object_id=self.id, amount=amount*-1)
            h.save()
            self.payed_price = amount
        super().save(*args, **kwargs)

class ContentProduct(models.Model):
    class Meta:
        unique_together = ('content', 'product')

    content = models.ForeignKey('Content', verbose_name=_('content'))
    product = models.ForeignKey('suppliers.Product', verbose_name=_('product'))
    quantity = models.PositiveIntegerField(_('quantity'), default=1)

    def __unicode__(self): return self.product.__unicode__()

class Content(models.Model):
    class Meta:
        unique_together = ('delivery', 'extent')

    delivery = models.ForeignKey('Delivery', verbose_name=_('delivery'))
    extent = models.ForeignKey('Extent', verbose_name=_('extent'))

    def __unicode__(self): return '%s, %s' % (self.delivery.__unicode__(), self.extent.__unicode__())

class Subscription(models.Model):
    customer = models.ForeignKey('customers.Customer', verbose_name=_('customer'))
    size = models.ForeignKey(Size, verbose_name=_('size'))
    frequency = models.PositiveIntegerField(_('frequency'), max_length=2, choices=FREQUENCY_CHOICES, default=FREQUENCY_DEFAULT, help_text=_('Delivery made sure Tuesday'))
    start = models.CharField(_('start'), max_length=7, choices=WEEKS_CHOICES,
                             help_text=_('Here is the beginnig week of the subscription.'))
    end = models.CharField(_('end'), max_length=7, choices=WEEKS_CHOICES,
                           help_text=_('Here is the ending week of the subscription.'))
    criterias = models.ManyToManyField('common.Criteria', null=True, blank=True, related_name='cart_subscription_criterias', verbose_name=_('criterias'))
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    direct_debit = models.BooleanField(_('direct debit'), default=True)
    enabled = models.BooleanField(_('enabled'), default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return '%s, %s, %s, %s, %s' % (self.customer.__unicode__(), self.size.name, self.get_frequency_display(), self.get_start_display(), self.get_end_display())

    def price(self): return self.size.default_price()

    def frequency_name(self): return dict(FREQUENCY_CHOICES).get(self.frequency)

    def duration(self):
        if not self.start or not self.end: return None
        s, e = Week.fromstring(self.start).day(1), Week.fromstring(self.end).day(1)
        return str(relativedelta(e,s))

    def duration2(self):
        if not self.start or not self.end: return None
        s, e = Week.fromstring(self.start).day(1), Week.fromstring(self.end).day(1)
        r = relativedelta(e,s)
        ret = ''
        if r.years: ret += _('%d years, ') % r.years
        if r.months: ret += _('%d months, ') % r.months
        if r.days: ret += _('%d days') % r.days
        return ret

    def create_deliveries(self):
        s, e = Week.fromstring(str(self.start)), Week.fromstring(str(self.end))
        for i in range(0, e+1-s, self.frequency):
            d = self.delivery_set.create(date=s+i)

class Extent(models.Model):
    class Meta:
        unique_together = ('subscription', 'product')

    subscription = models.ForeignKey(Subscription, verbose_name=_('subscription'))
    product = models.ForeignKey('products.Product', verbose_name=_('product'))
    extent = models.PositiveSmallIntegerField(_('extent'))

    def __unicode__(self): return '%s, %s, %s' % (self.subscription.__unicode__(), self.product.__unicode__(), self.extent)

class ThematicExtent(models.Model):
    class Meta:
        unique_together = ('thematic', 'product')

    thematic = models.ForeignKey(Thematic, verbose_name=_('thematic'))
    product = models.ForeignKey('products.Product', verbose_name=_('product'))
    extent = models.PositiveSmallIntegerField(_('extent'))

    def __unicode__(self): return '%s, %s, %s' % (self.thematic.__unicode__(), self.product.__unicode__(), self.extent)
