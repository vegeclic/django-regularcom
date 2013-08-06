from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self): return self.tag

class Category(models.Model):
    class Meta:
        verbose_name_plural = _('categories')

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    categories = models.ManyToManyField('self', null=True, blank=True, related_name='+')
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+')
    tags = generic.GenericRelation(TaggedItem)
    authors = models.ManyToManyField('accounts.Author', null=True, blank=True)

    def __unicode__(self): return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    categories = models.ManyToManyField(Category, null=True, blank=True, related_name='+')
    tags = generic.GenericRelation(TaggedItem)
    body = models.TextField(blank=True)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+')
    # authors = models.ManyToManyField('accounts.Author', null=True, blank=True, related_name='+')
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return self.name
