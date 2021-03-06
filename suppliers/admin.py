#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# Authors:
# Caner Candan <caner@candan.fr>, http://caner.candan.fr
# Geraldine Starke <geraldine@starke.fr>, http://www.vegeclic.fr
#

from django.contrib import admin
from django.contrib.contenttypes import generic
from modeltranslation.admin import TranslationAdmin
from . import forms, models
import common.admin as ca
import common.models as cm

class PriceInline(ca.LimitedAdminInlineMixin, admin.TabularInline):
    form = forms.PriceForm
    model = models.Price
    extra = 1

    def get_filters(self, obj): return (('supplier', {'product_suppliers': obj}),)

class SupplierFeeInline(admin.TabularInline):
    model = models.SupplierFee
    extra = 1

class SupplierAdmin(ca.MyModelAdmin):
    form = forms.SupplierForm
    add_form = forms.SupplierCreationForm
    list_display = ('id', 'name','fee_per_weight',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ca.AddressInline, ca.ImageInline, SupplierFeeInline,]

admin.site.register(models.Supplier, SupplierAdmin)

class IngredientAdmin(TranslationAdmin):
    list_display = ('id', 'name',)

admin.site.register(models.Ingredient, IngredientAdmin)

class ProductAdmin(TranslationAdmin):
    # form = forms.ProductForm
    # fields = ('name', 'slug', 'product', 'status', 'suppliers', 'criterias', 'body', 'ingredients', 'weight', 'sku', 'main_image', 'main_price')
    list_display = ('id', 'name', 'weight', 'date_created', 'date_last_modified', 'status',)
    list_filter = ('status',)
    search_fields = ('id', 'name', 'slug', 'weight', 'product__slug', 'main_price__reference',)
    filter_horizontal = ('suppliers', 'criterias',)
    actions = ['make_draft', 'make_published', 'make_expired', 'make_withdrawn',]
    inlines = [ca.ImageInline, PriceInline,]

    def make_draft(self, request, queryset): queryset.update(status='d')
    def make_published(self, request, queryset): queryset.update(status='p')
    def make_expired(self, request, queryset): queryset.update(status='e')
    def make_withdrawn(self, request, queryset): queryset.update(status='w')

admin.site.register(models.Product, ProductAdmin)

class InventoryInline(admin.TabularInline):
    model = models.Inventory
    extra = 3

class StoreAdmin(ca.MyModelAdmin):
    list_display = ('id', 'name', 'date_last_modified',)
    inlines = [InventoryInline, ca.AddressInline,]

admin.site.register(models.Store, StoreAdmin)

class EntryInline(admin.TabularInline):
    model = models.Entry
    extra = 3

class OrderAdmin(ca.MyModelAdmin):
    list_display = ('id', 'status', 'date_created', 'date_last_modified',)
    list_filter = ('status',)
    actions = ['make_draft', 'make_published', 'make_expired', 'make_withdrawn',]
    inlines = [EntryInline,]

    def make_draft(self, request, queryset): queryset.update(status='d')
    def make_validate(self, request, queryset): queryset.update(status='v')
    def make_expired(self, request, queryset): queryset.update(status='e')
    def make_withdrawn(self, request, queryset): queryset.update(status='w')

admin.site.register(models.Order, OrderAdmin)
