from django.contrib import admin
from django.contrib.contenttypes import generic
from . import forms, models
import common.admin as ca
import common.models as cm

class CurrencyAdmin(ca.MyModelAdmin):
    fieldsets = []
    list_display = ('name', 'symbol',)

admin.site.register(models.Currency, CurrencyAdmin)

class PriceInline(ca.LimitedAdminInlineMixin, admin.TabularInline):
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

class ProductAdmin(ca.MyModelAdmin):
    form = forms.ProductForm
    add_form = forms.ProductCreationForm
    list_display = ('name', 'weight', 'date_created', 'date_last_modified',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ca.ImageInline, PriceInline,]

    def queryset(self, request):
        qs = super(ca.MyModelAdmin, self).queryset(request)
        if request.user:
            return qs
        return qs.filter(author=request.user)

admin.site.register(models.Product, ProductAdmin)

class InventoryAdmin(ca.MyModelAdmin):
    list_display = ('product', 'quantity', 'date_last_modified',)

admin.site.register(models.Inventory, InventoryAdmin)

class EntryInline(admin.TabularInline):
    model = models.Entry
    extra = 3

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'product':
    #         print(db_field.blank)
    #         # kwargs['queryset'] = Product.objects.filter(owner=request.user)
    #     return super(EntryInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(admin.TabularInline, self).get_formset(request, obj, **kwargs)
        # f = formset.form.base_fields['product'].choices.choice()
        f = formset
        print(dir(f))
        print(f)
        # print([x for x in f])
        return formset

class OrderAdmin(ca.MyModelAdmin):
    list_display = ('date_created', 'date_last_modified',)
    inlines = [EntryInline,]

admin.site.register(models.Order, OrderAdmin)
