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
    inlines = [ImageInline, TaggedItemInline,]
    form = ProductForm
    list_display = ('name', 'date_created', 'date_last_modified',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Product, ProductAdmin)
