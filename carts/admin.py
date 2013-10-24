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
from hvad.admin import TranslatableAdmin
from isoweek import Week
from dateutil.relativedelta import relativedelta
from . import forms, models
import common.admin as ca
import common.models as cm

class ThematicExtentInline(admin.TabularInline):
    form = forms.ThematicExtentAdminForm
    model = models.ThematicExtent
    extra = 3

class ThematicAdmin(TranslatableAdmin):
    list_display = ('all_translations', 'name_', 'start_period', 'end_period', 'date_last_modified', 'enabled',)
    fields = ('name', 'body', 'size', 'locked_size', 'frequency', 'locked_frequency', 'start_duration', 'locked_start', 'end_duration', 'locked_duration', 'criterias', 'locked_criterias', 'locked_products', 'quantity', 'locked_quantity', 'start_period', 'end_period', 'main_image', 'enabled',)
    list_filter = ('enabled',)
    inlines = [ca.ImageInline, ThematicExtentInline,]

    def name_(self, obj): return obj.lazy_translation_getter('name')

admin.site.register(models.Thematic, ThematicAdmin)

class PriceInline(admin.TabularInline):
    form = forms.PriceAdminForm
    model = models.Price
    extra = 1

class CarrierLevelInline(admin.TabularInline):
    extra = 1
    model = models.CarrierLevel

class CarrierAdmin(TranslatableAdmin):
    extra = 1
    list_display = ('all_translations', 'name_', 'body_',)
    inlines = [CarrierLevelInline,]

    def name_(self, obj): return obj.lazy_translation_getter('name')
    def body_(self, obj): return obj.lazy_translation_getter('body')

admin.site.register(models.Carrier, CarrierAdmin)

class SizeAdmin(TranslatableAdmin):
    list_display = ('all_translations', 'name_', 'price', 'enabled',)
    fields = ('name', 'body', 'main_image', 'enabled',)
    inlines = [PriceInline, ca.ImageInline,]

    def name_(self, obj): return obj.lazy_translation_getter('name')

    def price(self, obj): return obj.price_set.get(currency=cm.Parameter.objects.get(name='default currency').content_object)

admin.site.register(models.Size, SizeAdmin)

class ExtentInline(admin.TabularInline):
    form = forms.ExtentAdminForm
    model = models.Extent
    extra = 3

class SubscriptionAdmin(ca.MyModelAdmin):
    add_form = forms.SubscriptionCreationAdminForm
    form = forms.SubscriptionAdminForm
    list_display = ('customer', 'size', 'frequency', 'duration', 'quantity', 'enabled',)
    list_filter = ('enabled',)
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
    # form = forms.ContentProductAdminForm
    model = models.ContentProduct
    extra = 3
    # fields = ('extent', 'proudct', 'quantity',)

    # def get_filters(self, obj): return (('content', {'extent__product': obj.product}),)
    def get_filters(self, obj): return (('product', {'product': obj}),)

class ContentAdmin(ca.MyModelAdmin):
    form = forms.ContentAdminForm
    model = models.Content
    # fields = ('extent', 'product', 'quantity',)
    list_display = ('delivery', 'extent',)
    inlines = [ContentProductInline,]

admin.site.register(models.Content, ContentAdmin)

class DeliveryAdmin(ca.MyModelAdmin):
    add_form = forms.DeliveryCreationAdminForm
    form = forms.DeliveryAdminForm
    list_display = ('subscription', 'date', 'status', 'payed_price',)
    list_filter = ('status',)
    # inlines = [ContentInline,]

admin.site.register(models.Delivery, DeliveryAdmin)
