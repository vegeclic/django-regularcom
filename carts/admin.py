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
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from modeltranslation.admin import TranslationAdmin
from isoweek import Week
from dateutil.relativedelta import relativedelta
from . import forms, models
import common.admin as ca
import common.models as cm

class ThematicExtentInline(admin.TabularInline):
    form = forms.ThematicExtentAdminForm
    model = models.ThematicExtent
    extra = 1

class ThematicAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'start_period', 'end_period', 'date_last_modified', 'enabled', 'order',)
    fields = ('name', 'body', 'size', 'locked_size', 'carrier', 'locked_carrier', 'receive_only_once', 'locked_receive_only_once', 'frequency', 'locked_frequency', 'start_duration', 'locked_start', 'end_duration', 'locked_duration', 'criterias', 'locked_criterias', 'locked_products', 'quantity', 'locked_quantity', 'start_period', 'end_period', 'main_image', 'enabled', 'order',)
    list_filter = ('enabled',)
    search_fields = ('name',)
    inlines = [ca.ImageInline, ThematicExtentInline,]

admin.site.register(models.Thematic, ThematicAdmin)

class PriceInline(admin.TabularInline):
    form = forms.PriceAdminForm
    model = models.Price
    extra = 1

class CarrierLevelInline(admin.TabularInline):
    extra = 1
    model = models.CarrierLevel

class CarrierAdmin(TranslationAdmin):
    extra = 1
    list_display = ('id', 'name', 'body', 'apply_suppliers_fee', 'weight_min', 'enabled',)
    fields = ('name', 'body', 'apply_suppliers_fee', 'weight_min', 'enabled',)
    inlines = [CarrierLevelInline,]

admin.site.register(models.Carrier, CarrierAdmin)

class SizeAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'price', 'weight', 'enabled', 'order',)
    fields = ('name', 'body', 'weight', 'main_image', 'enabled', 'order',)
    search_fields = ('name',)
    inlines = [PriceInline, ca.ImageInline,]

    def price(self, obj): return obj.price_set.get(currency=cm.Parameter.objects.get(name='default currency').content_object)

admin.site.register(models.Size, SizeAdmin)

class ExtentInline(admin.TabularInline):
    form = forms.ExtentAdminForm
    model = models.Extent
    extra = 1

class SubscriptionAdmin(ca.MyModelAdmin):
    add_form = forms.SubscriptionCreationAdminForm
    form = forms.SubscriptionAdminForm
    list_display = ('id', 'customer', 'size', 'carrier', 'receive_only_once', 'frequency', 'duration', 'quantity', 'enabled', 'date_created',)
    list_filter = ('enabled', 'receive_only_once', 'direct_debit', 'size', 'carrier', 'frequency',)
    search_fields = ('customer__account__email', 'customer__main_address__first_name', 'customer__main_address__last_name')
    ordering = ('-date_created',)
    filter_horizontal = ('criterias',)

    inlines = [ExtentInline,]

    def price(self, obj): return obj.size.price_set.get(currency=cm.Parameter.objects.get(name='default currency').content_object)

    def duration(self, obj):
        if not obj.start or not obj.end: return None
        s, e = Week.fromstring(obj.start).day(1), Week.fromstring(obj.end).day(1)
        return str(relativedelta(e,s))

    def nweeks(self, obj):
        if not obj.start or not obj.end: return None
        return Week.fromstring(obj.end) - Week.fromstring(obj.start)

admin.site.register(models.Subscription, SubscriptionAdmin)

class ContentProductInline(ca.LimitedAdminInlineMixin, admin.TabularInline):
    model = models.ContentProduct
    extra = 1

    # def get_filters(self, obj): return (('content', {'extent__product': obj.product}),)
    # def get_filters(self, obj): return (('product', {'product': obj}),)

class ContentAdmin(ca.MyModelAdmin):
    form = forms.ContentAdminForm
    list_display = ('id', 'delivery', 'product', 'extent', 'customized',)
    search_fields = ('delivery__subscription__customer__account__email', 'delivery__subscription__customer__main_address__first_name', 'delivery__subscription__customer__main_address__last_name')
    inlines = [ContentProductInline,]

admin.site.register(models.Content, ContentAdmin)

class DeliveryAdmin(ca.MyModelAdmin):
    add_form = forms.DeliveryCreationAdminForm
    form = forms.DeliveryAdminForm
    list_display = ('id', 'subscription', 'date', 'status', 'payed_price',)
    list_filter = ('status', 'subscription__enabled')
    search_fields = ('subscription__id', 'subscription__customer__account__email', 'subscription__customer__main_address__first_name', 'subscription__customer__main_address__last_name')
    ordering = ('date',)

admin.site.register(models.Delivery, DeliveryAdmin)

class ExtentContentProductInline(ca.LimitedAdminInlineMixin, admin.TabularInline):
    model = models.ExtentContentProduct
    extra = 1

    # def get_filters(self, obj): return (('product', {'product': obj}),)

class ExtentContentAdmin(ca.MyModelAdmin):
    form = forms.ExtentContentAdminForm
    list_display = ('id', 'extent',)
    inlines = [ExtentContentProductInline,]

admin.site.register(models.ExtentContent, ExtentContentAdmin)
