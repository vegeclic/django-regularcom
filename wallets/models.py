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

class Credit(models.Model):
    wallet = models.ForeignKey(Wallet, verbose_name=_('wallet'))
    PAYMENT_TYPES = (
        ('c', _('Cheque')),
        ('t', _('Bank transfer')),
        ('p', _('Paypal')),
    )
    payment_type = models.CharField(_('payment type'), max_length=1, choices=PAYMENT_TYPES, default='c')
    amount = models.FloatField(_('amount'), default=0)
    currency = models.ForeignKey('common.Currency', verbose_name=_('currency'))
    payment_date = models.DateField(_('payment date'), null=True, blank=True, help_text=_('This field may only be fullfilled for cheque payment.'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (
        ('d', _('Draft')),
        ('v', _('Validated')),
        ('e', _('Expired')),
        ('w', _('Withdrawn')),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')

    def __unicode__(self): return '%s, %s, %s, %s' % (self.wallet.__unicode__(), self.get_payment_type_display(), self.amount, self.date_created)

    def save(self, *args, **kwargs):
        if self.status == 'v':
            amount = self.amount / self.currency.exchange_rate
            self.wallet.balance += amount
            self.wallet.save()
            h = History(wallet=self.wallet, content_type=ContentType.objects.get(model='credit'),
                        object_id=self.id, amount=amount)
            h.save()
        super(Credit, self).save(*args, **kwargs)
