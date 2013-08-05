from django.contrib import admin
from .models import Category, Tag, Image, Currency, Price, Product
from .forms import ProductForm

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = []
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    fieldsets = []
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Tag, TagAdmin)

class ImageInline(admin.TabularInline):
    model = Image

class ImageAdmin(admin.ModelAdmin):
    fieldsets = []
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Image, ImageAdmin)

class CurrencyAdmin(admin.ModelAdmin):
    fieldsets = []
    list_display = ('name', 'symbol',)

admin.site.register(Currency, CurrencyAdmin)

class PriceAdmin(admin.ModelAdmin):
    fieldsets = []
    list_display = ('product', 'currency', 'price', 'selling_price',)

admin.site.register(Price, PriceAdmin)

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    form = ProductForm
    fieldsets = []
    list_display = ('name', 'main_category', 'quantity', 'date_created', 'date_last_modified',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Product, ProductAdmin)
