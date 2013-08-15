from django.contrib import admin
from django.contrib.contenttypes import generic
from hvad.admin import TranslatableAdmin
from . import forms, models
import common.admin as ca
import common.models as cm

class PriceInline(ca.LimitedAdminInlineMixin, admin.TabularInline):
    form = forms.PriceForm
    model = models.Price
    extra = 1

    def get_filters(self, obj): return (('supplier', {'product_suppliers': obj}),)

class SupplierAdmin(ca.MyModelAdmin):
    form = forms.SupplierForm
    add_form = forms.SupplierCreationForm
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ca.AddressInline, ca.ImageInline,]

admin.site.register(models.Supplier, SupplierAdmin)

class ProductAdmin(TranslatableAdmin):
    list_display = ('all_translations', 'name_', 'slug', 'weight', 'date_created', 'date_last_modified', 'status',)
    # list_display = ('name', 'weight', 'date_created', 'date_last_modified', 'status',)
    list_filter = ('status',)
    # prepopulated_fields = {"slug": ("name",)}
    actions = ['make_draft', 'make_published', 'make_expired', 'make_withdrawn',]
    inlines = [ca.ImageInline, PriceInline,]
    fields = ('name', 'slug', 'product', 'status', 'suppliers', 'criterias', 'body', 'weight', 'sku', 'main_image',)

    def name_(self, obj): return obj.lazy_translation_getter('name')

    def make_draft(self, request, queryset): queryset.update(status='d')
    def make_published(self, request, queryset): queryset.update(status='p')
    def make_expired(self, request, queryset): queryset.update(status='e')
    def make_withdrawn(self, request, queryset): queryset.update(status='w')

admin.site.register(models.Product, ProductAdmin)

class InventoryInline(admin.TabularInline):
    model = models.Inventory
    extra = 3

class StoreAdmin(ca.MyModelAdmin):
    list_display = ('name', 'date_last_modified',)
    inlines = [InventoryInline, ca.AddressInline,]

admin.site.register(models.Store, StoreAdmin)

class EntryInline(admin.TabularInline):
    model = models.Entry
    extra = 3

class OrderAdmin(ca.MyModelAdmin):
    list_display = ('status', 'date_created', 'date_last_modified',)
    list_filter = ('status',)
    actions = ['make_draft', 'make_published', 'make_expired', 'make_withdrawn',]
    inlines = [EntryInline,]

    def make_draft(self, request, queryset): queryset.update(status='d')
    def make_validate(self, request, queryset): queryset.update(status='v')
    def make_expired(self, request, queryset): queryset.update(status='e')
    def make_withdrawn(self, request, queryset): queryset.update(status='w')

admin.site.register(models.Order, OrderAdmin)
