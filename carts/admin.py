from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from . import forms, models
import common.admin as ca
import common.models as cm

class ThematicAdmin(ca.MyModelAdmin):
    form = forms.ThematicForm
    add_form = forms.ThematicCreationForm
    list_display = ('name', 'start_period', 'end_period', 'date_last_modified', 'status',)
    list_filter = ('status',)
    inlines = [ca.ImageInline,]

admin.site.register(models.Thematic, ThematicAdmin)

class PriceInline(admin.TabularInline):
    model = models.Price
    extra = 1

class SizeAdmin(ca.MyModelAdmin):
    form = forms.SizeForm
    add_form = forms.SizeCreationForm
    list_display = ('name', 'price',)
    inlines = [PriceInline, ca.ImageInline,]

    def price(self, obj): return obj.price_set.get(currency__name='Euro')

admin.site.register(models.Size, SizeAdmin)

class OrderAdmin(ca.MyModelAdmin):
    form = forms.OrderForm
    list_display = ('customer', 'size', 'price', 'frequency', 'start_period', 'end_period', 'quantity',)
    fieldsets = (
        (None,        {'fields': ['customer', 'size', 'frequency']}),
        (_('Period'), {'fields': ['start_period', 'end_period'], 'classes': ['collapse']}),
        (None,        {'fields': ['products', 'criterias', 'quantity']}),
    )

    def price(self, obj): return obj.size.price_set.get(currency__name='Euro')

admin.site.register(models.Order, OrderAdmin)
