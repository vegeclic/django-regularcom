from django.contrib import admin
from django.contrib.contenttypes import generic
from .models import Image, Country, Address

class CountryAdmin(admin.ModelAdmin):
    fieldsets = []
    list_display = ('name',)

admin.site.register(Country, CountryAdmin)

class AddressInline(generic.GenericStackedInline):
    model = Address
    extra = 1

class ImageInline(generic.GenericTabularInline):
    model = Image
    extra = 1
