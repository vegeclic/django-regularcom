from django.contrib import admin
from . import models, forms
import common.admin as ca

class CustomerAdmin(ca.MyModelAdmin):
    form = forms.CustomerForm
    add_form = forms.CustomerCreationForm
    fieldsets = []
    list_display = ('account', 'main_address', 'date_of_birth')
    inlines = [ca.AddressInline, ca.ImageInline,]

admin.site.register(models.Customer, CustomerAdmin)
