from django.contrib import admin
from .models import Customer
from .forms import CustomerForm
from common.admin import ImageInline, AddressInline

class CustomerAdmin(admin.ModelAdmin):
    inlines = [AddressInline,]
    form = CustomerForm
    fieldsets = []
    list_display = ('account', 'main_address', 'date_of_birth')

admin.site.register(Customer, CustomerAdmin)
