from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class Supplier(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True)
    delivery_delay = models.IntegerField(null=True, blank=True)
    threshold_order = models.IntegerField(null=True, blank=True)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+')

    def __unicode__(self): return self.name

class Currency(models.Model):
    class Meta:
        verbose_name_plural = _("currencies")

    name = models.CharField(max_length=30, unique=True)
    symbol = models.CharField(max_length=30, unique=True)

    def __unicode__(self): return ('%s (%s)' % (self.name, self.symbol)).strip()

class Price(models.Model):
    class Meta:
        unique_together = ('product', 'supplier', 'currency')

    product = models.ForeignKey('Product')
    supplier = models.ForeignKey(Supplier)
    currency = models.ForeignKey(Currency)
    purchase_price = models.FloatField()
    selling_price = models.FloatField(null=True, blank=True)

    def __unicode__(self): return ('%s%s %s' % (self.purchase_price, (' (%s)' % self.selling_price) if self.selling_price else '', self.currency.symbol)).strip()

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    product = models.ForeignKey('products.Product', related_name='+')
    body = models.TextField(blank=True)
    weight = models.FloatField(null=True, blank=True)
    sku = models.CharField(max_length=100, blank=True)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+')
    # authors = models.ManyToManyField('accounts.Author', null=True, blank=True, related_name='+')
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return self.name
