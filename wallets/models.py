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
from django.core.exceptions import ValidationError
import common.models as cm

class Wallet(models.Model):
    customer = models.OneToOneField('customers.Customer', verbose_name=_('customer'))
    balance = models.FloatField(_('balance'), default=0)
    target_currency = models.ForeignKey('common.Currency', verbose_name=_('target currency'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return self.customer.__unicode__()

    def balance_in_target_currency(self): return self.balance * self.target_currency.exchange_rate

class History(models.Model):
    class Meta:
        verbose_name_plural = _('histories')

    wallet = models.ForeignKey(Wallet, verbose_name=_('wallet'))
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(_('object id'), default=0)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    amount = models.FloatField(_('amount'), default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return '%s %s' % (self.wallet.__unicode__(), self.amount)

    def target_amount(self): return self.amount * self.wallet.target_currency.exchange_rate

PAYMENT_TYPES = (
    ('c', _('Cheque')),
    ('t', _('Bank transfer')),
    ('p', _('Paypal')),
)

STATUS_CHOICES = (
    ('w', _('In waiting')),
    ('v', _('Validated')),
    ('c', _('Canceled')),
    ('r', _('Rejected')),
)

class Credit(models.Model):
    wallet = models.ForeignKey(Wallet, verbose_name=_('wallet'))
    payment_type = models.CharField(_('payment type'), max_length=1, choices=PAYMENT_TYPES, default='c')
    amount = models.FloatField(_('amount'), default=0)
    currency = models.ForeignKey('common.Currency', verbose_name=_('currency'))
    payment_date = models.DateField(_('payment date'), null=True, blank=True, help_text=_('This field may only be fullfilled for cheque payment.'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='w')

    def amount_in_target_currency(self): return self.amount * self.wallet.target_currency.exchange_rate

    def __unicode__(self): return '%s, %s, %s, %s, %s' % (self.wallet.__unicode__(), self.get_payment_type_display(), self.amount, self.date_created, self.get_status_display())

    def save(self, *args, **kwargs):
        if self.status == 'v':
            self.wallet.balance += self.amount
            self.wallet.save()
            h = History(wallet=self.wallet, content_type=ContentType.objects.get(model='credit'),
                        object_id=self.id, amount=self.amount)
            h.save()
        super().save(*args, **kwargs)

class Withdraw(models.Model):
    wallet = models.ForeignKey(Wallet, verbose_name=_('wallet'))
    payment_type = models.CharField(_('payment type'), max_length=1, choices=PAYMENT_TYPES, default='c')
    amount = models.FloatField(_('amount'), default=0)
    currency = models.ForeignKey('common.Currency', verbose_name=_('currency'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='w')

    def amount_in_target_currency(self): return self.amount * self.wallet.target_currency.exchange_rate

    def __unicode__(self): return '%s, %s, %s, %s, %s' % (self.wallet.__unicode__(), self.get_payment_type_display(), self.amount, self.date_created, self.get_status_display())

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(self.status)
        if self.status == 'w':
            amount = abs(round(self.amount/self.currency.exchange_rate,2))
            if self.wallet.balance < amount:
                raise ValueError('There is not enough money in your wallet.')
            self.wallet.balance -= amount
            self.wallet.save()
        elif self.status == 'c':
            amount = abs(round(self.amount/self.currency.exchange_rate,2))
            self.wallet.balance += amount
            self.wallet.save()
        elif self.status == 'v':
            h = History(wallet=self.wallet, content_type=ContentType.objects.get(model='withdraw'),
                        object_id=self.id, amount=self.amount*-1)
            h.save()
