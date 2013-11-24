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

from django.contrib.contenttypes import generic
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from . import models, forms
import common.admin as ca

class TaggedItemInline(generic.GenericTabularInline):
    model = models.TaggedItem
    extra = 1

class CommentInline(admin.StackedInline):
    model = models.Comment
    extra = 1

class MicroblogInline(TranslationStackedInline):
    model = models.Microblog
    extra = 1

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if not field: return field
        if 'Message' in field.label: field.widget = forms.forms.Textarea()
        return field

class CategoryAdmin(TranslationAdmin):
    list_display = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(models.Category, CategoryAdmin)

class ArticleAdmin(TranslationAdmin):
    list_display = ('id', 'title', 'date_created', 'date_last_modified')
    ordering = ('-date_created',)
    filter_horizontal = ('authors', 'categories')
    inlines = [MicroblogInline, ca.ImageInline, TaggedItemInline, CommentInline,]

admin.site.register(models.Article, ArticleAdmin)

class ReaderAdmin(admin.ModelAdmin):
    list_display = ('account', 'number_of_articles_read',)
    filter_horizontal = ('articles_read',)

    def number_of_articles_read(self, obj): return obj.articles_read.count()

admin.site.register(models.Reader, ReaderAdmin)
