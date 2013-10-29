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
import mailbox.models as mm

class Wallet(models.Model):
    customer = models.OneToOneField('customers.Customer', verbose_name=_('customer'))
    balance = models.FloatField(_('balance'), default=0)
    target_currency = models.ForeignKey('common.Currency', verbose_name=_('target currency'))
    rib = models.CharField(_('RIB'), max_length=200, null=True, blank=True)
    payal = models.CharField(_('paypal'), max_length=200, null=True, blank=True)
    bitcoin = models.CharField(_('bitcoin'), max_length=200, null=True, blank=True)
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
    ('b', _('Bitcoin')),
)

STATUS_CHOICES = (
    ('w', _('Pending')),
    ('v', _('Validated')),
    ('c', _('Canceled')),
    ('r', _('Rejected')),
)

class Credit(models.Model):
    wallet = models.ForeignKey(Wallet, verbose_name=_('wallet'))
    payment_type = models.CharField(_('payment type'), max_length=1, choices=PAYMENT_TYPES, default='c', help_text=_('Select your payment type. For cheque and bank transfer, your wallet will be credited once received.'))
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

            mm.Message.objects.create_message(participants=[self.wallet.customer], subject=_("Requête d'approvisionnement d'un montant de %(amount)s %(amount_currency)s validée") % {'amount': self.amount_in_target_currency(), 'amount_currency': self.currency.symbol}, body=_(
"""Bonjour %(name)s,

Nous avons bien validé votre requête d'approvisionnement de votre compte d'un montant de %(amount)s %(amount_currency)s. Le nouveau solde de votre compte est de %(balance)s %(balance_currency)s.

Si vous avez déjà des abonnements en cours, les échéances seront automatiquement validés en fonction du nouveau solde disponible sur votre compte. Dans le cas contraire nous vous invitons, à présent, à créer un nouvel abonnement.

Bien cordialement,
Végéclic.
"""
            ) % {'name': self.wallet.customer.main_address.__unicode__() if self.wallet.customer.main_address else '', 'amount': self.amount_in_target_currency(), 'amount_currency': self.currency.symbol, 'balance': self.wallet.balance_in_target_currency(), 'balance_currency': self.wallet.target_currency.symbol})

        super().save(*args, **kwargs)

class Withdraw(models.Model):
    wallet = models.ForeignKey(Wallet, verbose_name=_('wallet'))
    payment_type = models.CharField(_('payment type'), max_length=1, choices=PAYMENT_TYPES, default='c', help_text=_('Select your payment type.'))
    amount = models.FloatField(_('amount'), default=0)
    currency = models.ForeignKey('common.Currency', verbose_name=_('currency'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='w')

    def amount_in_target_currency(self): return self.amount * self.wallet.target_currency.exchange_rate

    def __unicode__(self): return '%s, %s, %s, %s, %s' % (self.wallet.__unicode__(), self.get_payment_type_display(), self.amount, self.date_created, self.get_status_display())

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
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

            mm.Message.objects.create_message(participants=[self.wallet.customer], subject=_("Requête de retraits d'un montant de %(amount)s %(amount_currency)s validée") % {'amount': self.amount_in_target_currency(), 'amount_currency': self.currency.symbol}, body=_(
"""Bonjour %(name)s,

Nous avons bien validé votre requête de retraits de votre compte d'un montant de %(amount)s %(amount_currency)s. Le nouveau solde de votre compte est de %(balance)s %(balance_currency)s.

Vous allez recevoir prochainement votre paiement en fonction du type de paiement choisit.

Bien cordialement,
Végéclic.
"""
            ) % {'name': self.wallet.customer.main_address.__unicode__() if self.wallet.customer.main_address else '', 'amount': self.amount_in_target_currency(), 'amount_currency': self.currency.symbol, 'balance': self.wallet.balance_in_target_currency(), 'balance_currency': self.wallet.target_currency.symbol})
