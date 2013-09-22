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
from isoweek import Week
from dateutil.relativedelta import relativedelta
from . import forms, models
import common.admin as ca
import common.models as cm

class ThematicAdmin(ca.MyModelAdmin):
    form = forms.ThematicAdminForm
    add_form = forms.ThematicCreationAdminForm
    list_display = ('name', 'start_period', 'end_period', 'date_last_modified', 'enabled',)
    list_filter = ('enabled',)
    inlines = [ca.ImageInline,]

admin.site.register(models.Thematic, ThematicAdmin)

class PriceInline(admin.TabularInline):
    form = forms.PriceAdminForm
    model = models.Price
    extra = 1

class SizeAdmin(ca.MyModelAdmin):
    form = forms.SizeAdminForm
    add_form = forms.SizeCreationAdminForm
    list_display = ('name', 'price',)
    inlines = [PriceInline, ca.ImageInline,]

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
