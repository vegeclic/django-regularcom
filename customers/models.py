from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Customer(models.Model):
    account = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(null=True, blank=True)
    main_address = models.OneToOneField('common.Address', null=True, blank=True, related_name='+')
    shipping_address = models.OneToOneField('common.Address', null=True, blank=True, related_name='+')
    billing_address = models.OneToOneField('common.Address', null=True, blank=True, related_name='+')
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+')

    def __unicode__(self): return '%s%s' % (self.account.email, (' (%s)' % self.main_address.__unicode__()) if self.main_address else '')
