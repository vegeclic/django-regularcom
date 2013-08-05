from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Address(models.Model):
    account = models.ForeignKey(settings.AUTH_USER_MODEL)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=100, blank=True)
    home_phone = models.CharField(max_length=100, blank=True)
    mobile_phone = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

class Customer(models.Model):
    account = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(null=True, blank=True)
    main_address = models.OneToOneField(Address, null=True, blank=True, related_name='+')
    shipping_address = models.OneToOneField(Address, null=True, blank=True, related_name='+')
    billing_address = models.OneToOneField(Address, null=True, blank=True, related_name='+')

    def __unicode__(self):
        return self.account.email
