from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from common.models import Parameter

class Wallet(models.Model):
    customer = models.OneToOneField('customers.Customer', verbose_name=_('customer'))
    balance = models.FloatField(_('balance'), default=0)
    currency = models.ForeignKey('common.Currency', verbose_name=_('currency'),
                                 default=Parameter.objects.get(name='default currency').object_id)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
