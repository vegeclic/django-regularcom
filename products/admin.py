from django.contrib import admin
from django.contrib.contenttypes import generic
from . import models, forms
import common.admin as ca

class TaggedItemInline(generic.GenericTabularInline):
    model = models.TaggedItem
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    form = forms.CategoryForm
    add_form = forms.CategoryCreationForm
    inlines = [ca.ImageInline, TaggedItemInline,]
    fieldsets = []
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(models.Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    form = forms.ProductForm
    add_form = forms.ProductCreationForm
    list_display = ('name', 'date_created', 'date_last_modified', 'status',)
    list_filter = ('status',)
    prepopulated_fields = {"slug": ("name",)}
    actions = ['make_draft', 'make_published', 'make_expired', 'make_withdrawn',]
    inlines = [ca.ImageInline, TaggedItemInline,]

    def make_draft(self, request, queryset): queryset.update(status='d')
    def make_published(self, request, queryset): queryset.update(status='p')
    def make_expired(self, request, queryset): queryset.update(status='e')
    def make_withdrawn(self, request, queryset): queryset.update(status='w')

admin.site.register(models.Product, ProductAdmin)
