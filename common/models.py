from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class Image(models.Model):
    def image_name(self, filename):
        package = self.content_object.__module__.split('.')[0].lower()
        module = self.content_object.__class__.__name__.lower()
        slug = self.content_object.slug if 'slug' in dir(self.content_object) else str(self.object_id)
        return '/'.join([package, module, slug, filename])

    image = models.ImageField(upload_to=image_name)
    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self): return self.image

class Country(models.Model):
    class Meta:
        verbose_name_plural = 'Countries'

    name = models.CharField(max_length=30, unique=True)

    def __unicode__(self): return self.name

class Address(models.Model):
    content_type = models.ForeignKey(ContentType, related_name='+')
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    street = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    home_phone = models.CharField(max_length=100, blank=True)
    mobile_phone = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    def __unicode__(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
