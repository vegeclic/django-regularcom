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
from django.contrib.contenttypes import generic
from modeltranslation.admin import TranslationAdmin
from . import models, forms
import common.admin as ca

class TaggedItemInline(generic.GenericTabularInline):
    model = models.TaggedItem
    extra = 1

class CategoryAdmin(TranslationAdmin):
    # form = forms.CategoryForm
    # add_form = forms.CategoryCreationForm
    list_display = ('id', 'name',)
    fields = ('name', 'slug', 'categories', 'main_image', 'authors',)
    search_fields = ('name', 'slug',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ca.ImageInline, TaggedItemInline,]

admin.site.register(models.Category, CategoryAdmin)

class ProductAdmin(TranslationAdmin):
    # form = forms.ProductForm
    # add_form = forms.ProductCreationForm
    list_display = ('id', 'name', 'number_of_products', 'tax', 'date_created', 'date_last_modified', 'status',)
    list_filter = ('status',)
    search_fields = ('name', 'slug',)
    prepopulated_fields = {"slug": ("name",)}
    actions = ['make_draft', 'make_published', 'make_expired', 'make_withdrawn',]
    inlines = [ca.ImageInline, TaggedItemInline,]

    def number_of_products(self, obj): return len(obj.product_product.all())

    def make_draft(self, request, queryset): queryset.update(status='d')
    def make_published(self, request, queryset): queryset.update(status='p')
    def make_expired(self, request, queryset): queryset.update(status='e')
    def make_withdrawn(self, request, queryset): queryset.update(status='w')

admin.site.register(models.Product, ProductAdmin)
