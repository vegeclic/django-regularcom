from django.contrib import admin
from django.contrib.contenttypes import generic
from .models import Supplier, Currency, Price, Product, Inventory
from .forms import SupplierForm, ProductForm
from common.admin import ImageInline, AddressInline, LimitedAdminInlineMixin

class CurrencyAdmin(admin.ModelAdmin):
    fieldsets = []
    list_display = ('name', 'symbol',)

admin.site.register(Currency, CurrencyAdmin)

class PriceInline(LimitedAdminInlineMixin, admin.TabularInline):
    model = Price
    extra = 1

    def get_filters(self, obj): return (('supplier', {'product_suppliers': obj}),)

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

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'date_last_modified',)

admin.site.register(Inventory, InventoryAdmin)
