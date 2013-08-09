from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
import datetime
from common.models import Parameter

class StatusBasedModel(models.Model):
    STATUS_CHOICES = (
        ('d', _('Draft')),
        ('p', _('Published')),
        ('e', _('Expired')),
        ('w', _('Withdrawn')),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')

class Thematic(StatusBasedModel):
    name = models.CharField(max_length=100, unique=True)
    products = models.ManyToManyField('products.Product', null=True, blank=True, related_name='thematic_products')
    criterias = models.ManyToManyField('common.Criteria', null=True, blank=True, related_name='thematic_criterias')
    start_period = models.DateField(null=True, blank=True, default=datetime.date.today)
    end_period = models.DateField(null=True, blank=True)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+')
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

class Size(StatusBasedModel):
    name = models.CharField(max_length=100, unique=True)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+')

    def __unicode__(self): return '%s (%s)' % (self.name, self.price_set.get(currency__name='Euro').__unicode__())

class Price(models.Model):
    class Meta:
        unique_together = ('size', 'currency')

    size = models.ForeignKey(Size)
    currency = models.ForeignKey('common.Currency', related_name='cart_size_price_currency',
                                 default=Parameter.objects.get(name='default currency').object_id)
    price = models.FloatField()

    def __unicode__(self): return ('%s %s' % (self.price, self.currency.symbol)).strip()

class Order(models.Model):
    customer = models.ForeignKey('customers.Customer')
    size = models.ForeignKey(Size)
    FREQUENCY_CHOICES = (
        ('1', _('Once a week')),
        ('2', _('Every two weeks')),
        ('3', _('Every three weeks')),
        ('m', _('Once a month')),
        ('M', _('Every two months')),
        ('q', _('Once a quarter')),
        ('h', _('Every 6 months')),
        ('y', _('Once a year')),
    )
    frequency = models.CharField(max_length=1, choices=FREQUENCY_CHOICES, default='2', help_text=_('Delivery made sure Tuesday'))
    # weeks = models.CharField(max_length=2, choices=[(str(x),str(x)) for x in range(1,53)], default=datetime.date.today().isocalendar()[1])
    start_period = models.DateField(null=True, blank=True)
    end_period = models.DateField(null=True, blank=True)
    products = models.ManyToManyField('products.Product', null=True, blank=True, related_name='cart_order_products')
    criterias = models.ManyToManyField('common.Criteria', null=True, blank=True, related_name='cart_order_criterias')
    quantity = models.IntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return self.size.name
