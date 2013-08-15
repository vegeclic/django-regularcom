from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from hvad.models import TranslatableModel, TranslatedFields

class TaggedItem(models.Model):
    tag = models.SlugField(_('tag'))
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(_('object id'))
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self): return self.tag

class Category(TranslatableModel):
    class Meta:
        verbose_name_plural = _('categories')

    translations = TranslatedFields(
        name = models.CharField(_('name'), max_length=100, unique=True),
    )
    slug = models.SlugField(_('slug'), unique=True)
    categories = models.ManyToManyField('self', null=True, blank=True, related_name='+', verbose_name=_('categories'))
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+', verbose_name=_('main image'))
    tags = generic.GenericRelation(TaggedItem, verbose_name=_('tags'))
    authors = models.ManyToManyField('accounts.Author', null=True, blank=True, verbose_name=_('authors'))

    def __unicode__(self): return self.lazy_translation_getter('name', 'Category: %s' % self.pk)

class Product(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_('name'), max_length=100, unique=True),
        body = models.TextField(_('body'), blank=True),
    )
    slug = models.SlugField(_('slug'), unique=True)
    STATUS_CHOICES = (
        ('d', _('Draft')),
        ('p', _('Published')),
        ('e', _('Expired')),
        ('w', _('Withdrawn')),
    )
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='d')
    categories = models.ManyToManyField(Category, null=True, blank=True, related_name='+', verbose_name=_('categories'))
    tags = generic.GenericRelation(TaggedItem, verbose_name=_('tags'))
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+', verbose_name=_('main image'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return self.lazy_translation_getter('name', 'Category: %s' % self.pk)
