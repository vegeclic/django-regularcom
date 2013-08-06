from django.contrib import admin
from django.contrib.contenttypes import generic
from .models import Supplier, Currency, Price, Product
from .forms import SupplierForm, ProductForm
from common.admin import ImageInline, AddressInline

class CurrencyAdmin(admin.ModelAdmin):
    fieldsets = []
    list_display = ('name', 'symbol',)

admin.site.register(Currency, CurrencyAdmin)

class PriceInline(admin.TabularInline):
    model = Price
    extra = 1

class SupplierAdmin(admin.ModelAdmin):
    inlines = [AddressInline, ImageInline,]
    form = SupplierForm
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Supplier, SupplierAdmin)

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline, PriceInline,]
    form = ProductForm
    list_display = ('name', 'weight', 'date_created', 'date_last_modified',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Product, ProductAdmin)
