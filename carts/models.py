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
from django.contrib import messages
import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week
import common.models as cm
import wallets.models as wm
from mailbox import models as mm

FREQUENCY_CHOICES = (
    (1, _('Once a week')),
    (2, _('Every two weeks')),
    (3, _('Every three weeks')),
    (4, _('Once a month (4 weeks)')),
    (8, _('Every two months (8 weeks)')),
    (13, _('Once a quarter (13 weeks)')),
    (26, _('Every 6 months (26 weeks)')),
)

FREQUENCY_DEFAULT = 2

__weeks = []
for y in range(settings.START_YEAR, Week.thisweek().year+2): __weeks += Week.weeks_of_year(y)
WEEKS_CHOICES = [(str(w), '%s (%s %s)' % (w.day(settings.DELIVERY_DAY_OF_WEEK).strftime('%d-%m-%Y'), _('Week'), w.week)) for w in __weeks]

class Thematic(models.Model):
    name = models.CharField(_('name'), max_length=100)
    body = models.TextField(_('body'), blank=True)
    size = models.ForeignKey('Size', verbose_name=_('size'), null=True, blank=True)
    locked_size = models.BooleanField(_('locked size'), default=False)
    carrier = models.ForeignKey('Carrier', verbose_name=_('carrier'), null=True, blank=True)
    locked_carrier = models.BooleanField(_('locked carrier'), default=False)
    receive_only_once = models.BooleanField(_('receive only once'), default=False)
    locked_receive_only_once = models.BooleanField(_('locked receive only once'), default=False)
    frequency = models.PositiveIntegerField(_('frequency'), max_length=2, choices=FREQUENCY_CHOICES, help_text=_('Delivery made sure Tuesday'), null=True, blank=True)
    locked_frequency = models.BooleanField(_('locked frequency'), default=False)
    start_duration = models.CharField(_('start duration'), max_length=7, choices=WEEKS_CHOICES,
                                      help_text=_('Here is the beginnig week of the duration.'),
                                      null=True, blank=True)
    locked_start = models.BooleanField(_('locked start'), default=False)
    end_duration = models.CharField(_('end duration'), max_length=7, choices=WEEKS_CHOICES,
                                    help_text=_('Here is the ending week of the duration.'),
                                    null=True, blank=True)
    locked_duration = models.BooleanField(_('locked duration'), default=False)
    criterias = models.ManyToManyField('common.Criteria', null=True, blank=True, related_name='thematic_criterias', verbose_name=_('criterias'))
    locked_criterias = models.BooleanField(_('locked criterias'), default=False)
    locked_products = models.BooleanField(_('locked products'), default=False)
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    locked_quantity = models.BooleanField(_('locked quantity'), default=False)
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
    order = models.IntegerField(_('order'), default=0)

    def __unicode__(self): return self.name

class Size(models.Model):
    name = models.CharField(_('name'), max_length=100)
    body = models.TextField(_('body'), blank=True)
    weight = models.FloatField(_('weight'))
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+', verbose_name=_('main image'))
    enabled = models.BooleanField(_('enabled'), default=False)

    def default_price(self):
        try:
            return self.price_set.get(currency__name=settings.DEFAULT_CURRENCY)
        except Size.DoesNotExist:
            return None

    def __unicode__(self):
        price = self.default_price()
        # return '%s%s' % (name, (' (%s)' % (price.__unicode__())) if price else "")
        return price.__unicode__()

class Price(models.Model):
    class Meta:
        unique_together = ('size', 'currency')

    size = models.ForeignKey(Size, verbose_name=_('size'))
    currency = models.ForeignKey('common.Currency', related_name='cart_size_price_currency', verbose_name=_('currency'))
    price = models.FloatField(_('price'))

    def __unicode__(self): return ('%s %s' % (self.price, self.currency.symbol)).strip()

class Carrier(models.Model):
    name = models.CharField(_('name'), max_length=100)
    body = models.TextField(_('body'), blank=True)
    apply_suppliers_fee = models.BooleanField(_('apply suppliers fee'), default=True)
    weight_min = models.FloatField(_('weight min'), default=0)
    enabled = models.BooleanField(_('enabled'), default=True)

    def __unicode__(self): return self.name

class CarrierLevel(models.Model):
    class Meta:
        unique_together = ('carrier', 'weight', 'currency')

    carrier = models.ForeignKey(Carrier, verbose_name=_('carrier'))
    weight = models.FloatField(_('weight'))
    currency = models.ForeignKey('common.Currency', related_name='cart_carrier_level_price_currency', verbose_name=_('currency'))
    price = models.FloatField(_('price'))

    def __unicode__(self): return '%.2f %s / %.2f kg' % (self.price, self.currency.symbol, self.weight)

class Delivery(models.Model):
    class Meta:
        verbose_name_plural = _('deliveries')

    subscription = models.ForeignKey('Subscription', verbose_name=_('subscription'))
    date = models.CharField(_('date'), max_length=7, choices=WEEKS_CHOICES)
    STATUS_CHOICES = (
        ('w', _('Pending')),
        ('p', _('Payed')),
        ('P', _('In progress')),
        ('s', _('Sent')),
        ('d', _('Delivered')),
        ('c', _('Canceled')),
        ('e', _('Expired')),
    )
    SUCCESS_CHOICES = ['p', 'P', 's', 'd']
    FAILED_CHOICES = ['c', 'e']
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='w')
    payed_price = models.FloatField(_('payed price'), null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return '%s - %s' % (self.subscription.__unicode__(), self.get_date_display())

    def save(self, *args, **kwargs):
        if self.status == 'p':
            customer = self.subscription.customer
            wallet = customer.wallet
            payed_deliveries = self.subscription.delivery_set.filter(status__in=self.SUCCESS_CHOICES)
            self.payed_price = self.subscription.price().price/(1+settings.DEGRESSIVE_PRICE_RATE/100)**len(payed_deliveries.all())
            if wallet.balance < self.payed_price:
                message = mm.Message.objects.create_message(participants=[customer], subject=_('Delivery %(date)s cannot be validated') % {'date': self.get_date_display()}, body=_(
"""Hi %(name)s,

with some regret I must report that we were unable to validate your delivery %(date)s from the subscription %(subscription_id)d since you dont have enough money in your wallet to buy it.

Please take a moment to credit your wallet first and validate the delivery back.

Best regards,
Végéclic.
"""
                ) % {'name': customer.main_address.__unicode__() if customer.main_address else '', 'date': self.get_date_display(), 'subscription_id': self.subscription.id})

                raise ValueError(_('You dont have enough money in your wallet to buy it.'))

            wallet.balance -= self.payed_price
            wallet.save()

            h = wm.History(wallet=wallet, content_type=ContentType.objects.get(model='delivery'),
                           object_id=self.id, amount=self.payed_price*-1)

            message = mm.Message.objects.create_message(participants=[customer], subject=_('Delivery %(date)s has been validated') % {'date': self.get_date_display()}, body=_(
"""Hi %(name)s,

we are pleased to announce your delivery %(date)s from the subscription %(subscription_id)d has been validated automatically.

Your cart will be prepared as soon as possible and send to you in 10-12 days.

Best regards,
Végéclic.
"""
            ) % {'name': customer.main_address.__unicode__() if customer.main_address else '', 'date': self.get_date_display(), 'subscription_id': self.subscription.id})

            h.save()
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
        unique_together = ('delivery', 'product')

    delivery = models.ForeignKey('Delivery', verbose_name=_('delivery'))
    product = models.ForeignKey('products.Product', verbose_name=_('product'))
    extent = models.PositiveSmallIntegerField(_('extent'), default=0)
    customized = models.BooleanField(_('customized'), default=False)

    def __unicode__(self): return '%s, %s, %d' % (self.delivery.__unicode__(), self.product.__unicode__(), self.extent)

class Subscription(models.Model):
    customer = models.ForeignKey('customers.Customer', verbose_name=_('customer'))
    size = models.ForeignKey(Size, verbose_name=_('size'))
    carrier = models.ForeignKey(Carrier, verbose_name=_('carrier'))
    receive_only_once = models.BooleanField(_('receive only once'), default=False)
    frequency = models.PositiveIntegerField(_('frequency'), max_length=2, choices=FREQUENCY_CHOICES, default=FREQUENCY_DEFAULT, help_text=_('Delivery made sure Tuesday'))
    start = models.CharField(_('start'), max_length=7, choices=WEEKS_CHOICES,
                             help_text=_('Here is the beginnig week of the subscription.'))
    end = models.CharField(_('end'), max_length=7, choices=WEEKS_CHOICES,
                           help_text=_('Here is the ending week of the subscription.'))
    criterias = models.ManyToManyField('common.Criteria', null=True, blank=True, related_name='cart_subscription_criterias', verbose_name=_('criterias'))
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    direct_debit = models.BooleanField(_('direct debit'), default=True)
    enabled = models.BooleanField(_('enabled'), default=True)
    comment = models.TextField(_('comment'), null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        if not self.receive_only_once:
            return '%d, %s, %s, %s, %s, %s' % (self.id, self.customer.__unicode__(), self.size.name, self.get_frequency_display(), self.get_start_display(), self.get_end_display())
        return '%d, %s, %s, %s' % (self.id, self.customer.__unicode__(), self.size.name, self.get_start_display())

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
        if self.receive_only_once:
            d = self.delivery_set.create(date=s)
        else:
            for i in range(0, e+1-s, self.frequency):
                d = self.delivery_set.create(date=s+i)

class Extent(models.Model):
    class Meta:
        unique_together = ('subscription', 'product')

    subscription = models.ForeignKey(Subscription, verbose_name=_('subscription'))
    product = models.ForeignKey('products.Product', verbose_name=_('product'))
    extent = models.PositiveSmallIntegerField(_('extent'))
    customized = models.BooleanField(_('customized'), default=False)

    def __unicode__(self): return '%s, %s, %s' % (self.subscription.__unicode__(), self.product.__unicode__(), self.extent)

class ExtentContent(models.Model):
    extent = models.ForeignKey('Extent', verbose_name=_('extent'), unique=True)

class ExtentContentProduct(models.Model):
    class Meta:
        unique_together = ('content', 'product')

    content = models.ForeignKey('ExtentContent', verbose_name=_('content'))
    product = models.ForeignKey('suppliers.Product', verbose_name=_('product'))
    quantity = models.PositiveIntegerField(_('quantity'), default=1)

    def __unicode__(self): return self.product.__unicode__()

class ThematicExtent(models.Model):
    class Meta:
        unique_together = ('thematic', 'product')

    thematic = models.ForeignKey(Thematic, verbose_name=_('thematic'))
    product = models.ForeignKey('products.Product', verbose_name=_('product'))
    extent = models.PositiveSmallIntegerField(_('extent'))

    def __unicode__(self): return '%s, %s, %s' % (self.thematic.__unicode__(), self.product.__unicode__(), self.extent)
