from django.contrib import admin
from .models import Address, Customer
from .forms import CustomerForm

class AddressAdmin(admin.ModelAdmin):
    fieldsets = []

admin.site.register(Address, AddressAdmin)

class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
    fieldsets = []
    list_display = ('account', 'main_address', 'date_of_birth')

admin.site.register(Customer, CustomerAdmin)
