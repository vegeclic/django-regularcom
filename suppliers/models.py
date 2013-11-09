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
import common.models as cm
import numpy as np

class Supplier(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    suppliers = models.ManyToManyField('self', null=True, blank=True, related_name='supplier_suppliers', verbose_name=_('suppliers'))
    delivery_delay = models.PositiveIntegerField(_('delivery delay'), null=True, blank=True)
    threshold_order = models.PositiveIntegerField(_('threshold order'), null=True, blank=True)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+', verbose_name=_('main image'))

    def __unicode__(self): return self.name

    def fee_per_weight(self):
        try:
            return self.supplierfee_set.get(currency__name=settings.DEFAULT_CURRENCY)
        except Supplier.DoesNotExist:
            return None

class SupplierFee(models.Model):
    class Meta:
        unique_together = ('supplier', 'currency')

    supplier = models.ForeignKey(Supplier, verbose_name=_('supplier'))
    currency = models.ForeignKey('common.Currency', related_name='supplier_fee_currency', verbose_name=_('currency'))
    fee_per_weight = models.FloatField(_('fee per weight'))

    def __unicode__(self): return '%s %s / 1 kg' % (self.fee_per_weight, self.currency.symbol)

class Product(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_('name'), max_length=100),
        slug = models.SlugField(max_length=100, null=True, blank=True),
        body = models.TextField(_('body'), blank=True),
        ingredients = models.TextField(_('ingredients'), blank=True),
    )
    product = models.ForeignKey('products.Product', related_name='product_product', verbose_name=_('product'))
    STATUS_CHOICES = (
        ('d', _('Draft')),
        ('p', _('Published')),
        ('o', _('Out of stock')),
        ('e', _('Expired')),
        ('w', _('Withdrawn')),
    )
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='d')
    suppliers = models.ManyToManyField(Supplier, null=True, blank=True, related_name='product_suppliers', verbose_name=_('suppliers'))
    criterias = models.ManyToManyField('common.Criteria', null=True, blank=True, related_name='product_criterias', verbose_name=_('criterias'))
    weight = models.FloatField(_('weight'), null=True, blank=True)
    sku = models.CharField(max_length=100, blank=True)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+', verbose_name=_('main image'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return '%s, %s' % (self.lazy_translation_getter('name', 'Product: %s' % self.pk), self.price().purchase_price)

    def price(self):
        try:
            return self.price_set.select_related('currency', 'tax').get(currency__name=settings.DEFAULT_CURRENCY)
        except Product.DoesNotExist:
            return None

class Tax(models.Model):
    class Meta:
        verbose_name_plural = _('taxes')

    name = models.CharField(_('name'), max_length=100, null=True, blank=True)
    rate = models.FloatField(_('rate'))

    def __unicode__(self): return self.name

class Price(models.Model):
    class Meta:
        unique_together = ('product', 'supplier', 'currency')

    product = models.ForeignKey(Product, verbose_name=_('product'))
    supplier = models.ForeignKey(Supplier, verbose_name=_('supplier'))
    reference = models.CharField(_('reference'), max_length=30, null=True, blank=True)
    supplier_product_url = models.URLField(_('supplier product url'), null=True, blank=True)
    limited = models.BooleanField(_('limited product'), default=False)
    currency = models.ForeignKey('common.Currency', related_name='supplier_product_price_currency', verbose_name=_('currency'))
    purchase_price = models.FloatField(_('purchase price'))
    selling_price = models.FloatField(_('selling price'), null=True, blank=True)
    tax = models.ForeignKey(Tax, related_name='supplier_product_price_tax', verbose_name=_('tax'), null=True, blank=True)

    def price(self): return self.selling_price if self.selling_price else self.purchase_price

    def margin_price(self): return round(self.selling_price if self.selling_price else (self.purchase_price * (1+settings.PRICE_MARGIN_RATE/100)), 2)

    def get_pre_tax_price(self): return self.margin_price()

    def get_after_tax_price(self): return round(self.get_pre_tax_price() * ((1+self.tax.rate/100) if self.tax else 1), 2)

    def get_after_tax_price_with_fee(self): return round(self.get_after_tax_price() + (self.product.weight/1000) * self.supplier.fee_per_weight().fee_per_weight, 2)

    def pro_margin_price(self): return round(self.selling_price if self.selling_price else (self.purchase_price * (1+settings.PRICE_PRO_MARGIN_RATE/100)), 2)

    def get_pro_pre_tax_price(self): return self.pro_margin_price()

    def get_pro_after_tax_price(self): return round(self.get_pro_pre_tax_price() * ((1+self.tax.rate/100) if self.tax else 1), 2)

    def degressive_price(self, nb_deliveries=52):
        values = []
        for i in range(nb_deliveries):
            values.append(self.get_after_tax_price()/(1+settings.DEGRESSIVE_PRICE_RATE/100)**i)
        return round(np.mean(values), 2)

    def __unicode__(self):
        return ('%.2f %s' % (self.get_after_tax_price(), self.currency.symbol)).strip()

    def price_pro(self):
        return ('%.2f %s' % (self.get_pro_after_tax_price(), self.currency.symbol)).strip()

class Inventory(models.Model):
    class Meta:
        verbose_name_plural = _('inventories')

    store = models.ForeignKey('Store', verbose_name=_('store'))
    product = models.OneToOneField(Product, verbose_name=_('product'))
    quantity = models.PositiveIntegerField(_('quantity'), null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return self.product.name

class Store(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return self.name

class Entry(models.Model):
    class Meta:
        verbose_name_plural = _('entries')

    order = models.ForeignKey('Order', verbose_name=_('order'))
    product = models.OneToOneField(Product, verbose_name=_('product'))
    quantity = models.PositiveIntegerField(_('quantity'), null=True, blank=True)

    def __unicode__(self): return self.product.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('d', _('Draft')),
        ('v', _('Validated')),
        ('e', _('Expired')),
        ('w', _('Withdrawn')),
    )
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='d')
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
