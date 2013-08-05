from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    class Meta:
        verbose_name_plural = _("categories")

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    authors = models.ManyToManyField('accounts.Author', null=True, blank=True)

    def __unicode__(self): return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    authors = models.ManyToManyField('accounts.Author', null=True, blank=True)

    def __unicode__(self): return self.name

class Image(models.Model):
    def image_name(instance, filename):
        return '/'.join(['product', instance.slug, filename])

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=image_name)
    authors = models.ManyToManyField('accounts.Author', null=True, blank=True)

    def __unicode__(self): return self.name

class Currency(models.Model):
    class Meta:
        verbose_name_plural = _("currencies")

    name = models.CharField(max_length=30, unique=True)
    symbol = models.CharField(max_length=30, unique=True)

    def __unicode__(self): return ('%s (%s)' % (self.name, self.symbol)).strip()

class Price(models.Model):
    class Meta:
        unique_together = ('product', 'currency')

    product = models.ForeignKey('Product')
    currency = models.ForeignKey(Currency)
    price = models.FloatField()
    selling_price = models.FloatField(null=True, blank=True)

    def __unicode__(self): return ('%s%s %s' % (self.price, (' (%s)' % self.selling_price) if self.selling_price else '', self.currency.symbol)).strip()

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    main_category = models.ForeignKey(Category)
    other_categories = models.ManyToManyField(Category, null=True, blank=True, related_name='+')
    tags = models.ManyToManyField(Tag, null=True, blank=True, related_name='+')
    body = models.TextField(blank=True)
    prices = models.ManyToManyField(Price, null=True, blank=True, related_name='+')
    quantity = models.IntegerField(null=True, blank=True)
    image = models.ForeignKey(Image, null=True, blank=True)
    other_images = models.ManyToManyField(Image, null=True, blank=True, related_name='+')
    authors = models.ManyToManyField('accounts.Author', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return self.name
