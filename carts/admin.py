from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from isoweek import Week
from dateutil.relativedelta import relativedelta
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
    form = forms.PriceForm
    model = models.Price
    extra = 1

class SizeAdmin(ca.MyModelAdmin):
    form = forms.SizeForm
    add_form = forms.SizeCreationForm
    list_display = ('name', 'price',)
    inlines = [PriceInline, ca.ImageInline,]

    def price(self, obj): return obj.price_set.get(currency=cm.Parameter.objects.get(name='default currency').content_object)

admin.site.register(models.Size, SizeAdmin)

class ExtentInline(admin.TabularInline):
    form = forms.ExtentForm
    model = models.Extent
    extra = 3

class SubscriptionAdmin(ca.MyModelAdmin):
    add_form = forms.SubscriptionCreationForm
    form = forms.SubscriptionForm
    list_display = ('customer', 'size', 'price', 'frequency', 'nweeks', 'duration', 'quantity', 'status',)
    list_filter = ('status',)
    inlines = [ExtentInline,]

    def price(self, obj): return obj.size.price_set.get(currency=cm.Parameter.objects.get(name='default currency').content_object)

    def duration(self, obj):
        s, e = Week.fromstring(obj.start).day(1), Week.fromstring(obj.end).day(1)
        return str(relativedelta(e,s))

    def nweeks(self, obj): return Week.fromstring(obj.end) - Week.fromstring(obj.start)

admin.site.register(models.Subscription, SubscriptionAdmin)

class ContentProductInline(ca.LimitedAdminInlineMixin, admin.TabularInline):
    # form = forms.ContentProductForm
    model = models.ContentProduct
    extra = 3
    # fields = ('extent', 'product', 'quantity',)

    # def get_filters(self, obj): return (('content', {'extent__product': obj.product}),)
    def get_filters(self, obj): return (('product', {'product': obj}),)

class ContentAdmin(ca.MyModelAdmin):
    form = forms.ContentForm
    model = models.Content
    # fields = ('extent', 'product', 'quantity',)
    list_display = ('delivery', 'extent',)
    inlines = [ContentProductInline,]

admin.site.register(models.Content, ContentAdmin)

class DeliveryAdmin(ca.MyModelAdmin):
    add_form = forms.DeliveryCreationForm
    form = forms.DeliveryForm
    list_display = ('subscription', 'date', 'status',)
    list_filter = ('status',)
    # inlines = [ContentInline,]

admin.site.register(models.Delivery, DeliveryAdmin)
