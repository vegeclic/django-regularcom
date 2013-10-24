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
from hvad.models import TranslatableModel, TranslatedFields
import common.models as cm

class Supplier(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    suppliers = models.ManyToManyField('self', null=True, blank=True, related_name='supplier_suppliers', verbose_name=_('suppliers'))
    delivery_delay = models.PositiveIntegerField(_('delivery delay'), null=True, blank=True)
    threshold_order = models.PositiveIntegerField(_('threshold order'), null=True, blank=True)
    # fee_per_weight = models.FloatField(_('fee per weight'), default=0, null=True, blank=True)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+', verbose_name=_('main image'))

    def __unicode__(self): return self.name

    def fee_per_weight(self):
        try:
            return self.supplierfee_set.get(currency=cm.Parameter.objects.get(name='default currency').content_object)
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
        name = models.CharField(_('name'), max_length=100, unique=True),
        body = models.TextField(_('body'), blank=True),
        ingredients = models.TextField(_('ingredients'), blank=True),
    )
    slug = models.SlugField(unique=True, max_length=100)
    product = models.ForeignKey('products.Product', related_name='product_product', verbose_name=_('product'))
    STATUS_CHOICES = (
        ('d', _('Draft')),
        ('p', _('Published')),
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

    # def origin(self):
    #     try:
    #         return self.price_set.get(currency=cm.Parameter.objects.get(name='default currency').content_object).origin()
    #     except Product.DoesNotExist:
    #         return None

    def price(self):
        try:
            return self.price_set.get(currency=cm.Parameter.objects.get(name='default currency').content_object)
        except Product.DoesNotExist:
            return None

class Fee(models.Model):
    name = models.CharField(_('name'), max_length=100, null=True, blank=True)
    percent = models.FloatField(_('percent'))

    def __unicode__(self): return self.name

class Price(models.Model):
    class Meta:
        unique_together = ('product', 'supplier', 'currency')

    product = models.ForeignKey(Product, verbose_name=_('product'))
    supplier = models.ForeignKey(Supplier, verbose_name=_('supplier'))
    reference = models.CharField(_('reference'), max_length=30, null=True, blank=True)
    supplier_product_url = models.URLField(_('supplier product url'), null=True, blank=True)
    currency = models.ForeignKey('common.Currency', related_name='supplier_product_price_currency', verbose_name=_('currency'))
    purchase_price = models.FloatField(_('purchase price'))
    selling_price = models.FloatField(_('selling price'), null=True, blank=True)
    fee = models.ForeignKey(Fee, related_name='supplier_product_price_fee', verbose_name=_('fee'), null=True, blank=True)

    # def __unicode__(self): return ('%s%s %s' % (self.purchase_price, (' (%s)' % self.selling_price) if self.selling_price else '', self.currency.symbol)).strip()

    def __unicode__(self): return ('%.2f (%.2f) %s' % (self.purchase_price, self.purchase_price * (1+(.50+.055+(self.fee.percent/100))), self.currency.symbol)).strip()

    # def fees(self): return ('%s%s %s' % (self.purchase_price * (1+(.5+.05+.055)), (' (%s)' % self.selling_price) if self.selling_price else '', self.currency.symbol)).strip()

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
