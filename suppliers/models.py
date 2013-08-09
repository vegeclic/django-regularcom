from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from common.models import Parameter

class Supplier(models.Model):
    name = models.CharField(_('name'), max_length=30, unique=True)
    slug = models.SlugField(unique=True)
    delivery_delay = models.IntegerField(_('delivery delay'), null=True, blank=True)
    threshold_order = models.IntegerField(_('threshold order'), null=True, blank=True)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+', verbose_name=_('main image'))

    def __unicode__(self): return self.name

class Product(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    product = models.ForeignKey('products.Product', related_name='+', verbose_name=_('product'))
    STATUS_CHOICES = (
        ('d', _('Draft')),
        ('p', _('Published')),
        ('e', _('Expired')),
        ('w', _('Withdrawn')),
    )
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='d')
    suppliers = models.ManyToManyField(Supplier, null=True, blank=True, related_name='product_suppliers', verbose_name=_('suppliers'))
    criterias = models.ManyToManyField('common.Criteria', null=True, blank=True, related_name='product_criterias', verbose_name=_('criterias'))
    body = models.TextField(_('body'), blank=True)
    weight = models.FloatField(_('weight'), null=True, blank=True)
    sku = models.CharField(max_length=100, blank=True)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+', verbose_name=_('main image'))
    # authors = models.ManyToManyField('accounts.Author', null=True, blank=True, related_name='+', verbose_name=_('authors'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return self.name

class Price(models.Model):
    class Meta:
        unique_together = ('product', 'supplier', 'currency')

    product = models.ForeignKey(Product, verbose_name=_('product'))
    supplier = models.ForeignKey(Supplier, verbose_name=_('supplier'))
    currency = models.ForeignKey('common.Currency', related_name='supplier_product_price_currency', verbose_name=_('currency'), default=Parameter.objects.get(name='default currency').object_id)
    purchase_price = models.FloatField(_('purchase price'))
    selling_price = models.FloatField(_('selling price'), null=True, blank=True)

    def __unicode__(self): return ('%s%s %s' % (self.purchase_price, (' (%s)' % self.selling_price) if self.selling_price else '', self.currency.symbol)).strip()

class Inventory(models.Model):
    class Meta:
        verbose_name_plural = _('inventories')

    store = models.ForeignKey('Store', verbose_name=_('store'))
    product = models.OneToOneField(Product, verbose_name=_('product'))
    quantity = models.IntegerField(_('quantity'), null=True, blank=True)
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
    quantity = models.IntegerField(_('quantity'), null=True, blank=True)

    def __unicode__(self): return self.product.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('d', _('Draft')),
        ('v', _('Validate')),
        ('e', _('Expired')),
        ('w', _('Withdrawn')),
    )
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='d')
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
