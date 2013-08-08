from django.contrib import admin
from django.contrib.contenttypes import generic
from .models import Category, TaggedItem, Product
from .forms import ProductForm
from common.admin import ImageInline

class TaggedItemInline(generic.GenericTabularInline):
    model = TaggedItem
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ImageInline, TaggedItemInline,]
    fieldsets = []
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('name', 'date_created', 'date_last_modified', 'status',)
    list_filter = ('status',)
    prepopulated_fields = {"slug": ("name",)}
    actions = ['make_draft', 'make_published', 'make_expired', 'make_withdrawn',]
    inlines = [ImageInline, TaggedItemInline,]

    def make_draft(self, request, queryset): queryset.update(status='d')
    def make_published(self, request, queryset): queryset.update(status='p')
    def make_expired(self, request, queryset): queryset.update(status='e')
    def make_withdrawn(self, request, queryset): queryset.update(status='w')

admin.site.register(Product, ProductAdmin)
