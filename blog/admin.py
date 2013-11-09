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
from hvad.admin import TranslatableAdmin
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from . import models
import common.admin as ca

class TaggedItemInline(generic.GenericTabularInline):
    model = models.TaggedItem
    extra = 1

class CommentInline(admin.StackedInline):
    model = models.Comment
    extra = 1

class CategoryAdmin(TranslatableAdmin):
    list_display = ('id', 'all_translations', 'name_')

    def name_(self, obj): return obj.lazy_translation_getter('name')

admin.site.register(models.Category, CategoryAdmin)

class ArticleAdmin(TranslatableAdmin):
    list_display = ('id', 'all_translations', 'title_', 'date_created', 'date_last_modified')
    ordering = ('-date_created',)
    filter_horizontal = ('authors', 'categories')
    inlines = [CommentInline, ca.ImageInline, TaggedItemInline,]

    def title_(self, obj): return obj.lazy_translation_getter('title')

admin.site.register(models.Article, ArticleAdmin)
