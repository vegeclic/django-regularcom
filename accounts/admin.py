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
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from . import models, forms
import common.admin as ca

class AccountAdmin(UserAdmin):
    form = forms.AccountChangeAdminForm
    add_form = forms.AccountCreationAdminForm
    list_display = ('id', 'email', 'is_admin', 'date_created', 'last_login',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('-date_created',)
    filter_horizontal = ()

admin.site.register(models.Account, AccountAdmin)
admin.site.unregister(Group)

class AuthorAdmin(ca.MyModelAdmin):
    add_form = forms.AuthorCreationForm
    form = forms.AuthorForm
    fieldsets = []
    list_display = ('id', 'name',)
    inlines = [ca.ImageInline,]

admin.site.register(models.Author, AuthorAdmin)
