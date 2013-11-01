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
from . import models, forms
import common.admin as ca

class CustomerAdmin(ca.MyModelAdmin):
    form = forms.CustomerForm
    add_form = forms.CustomerCreationForm
    fieldsets = []
    list_display = ('id', 'account', 'main_address', 'date_of_birth', 'date_created',)
    search_fields = ('account__email', 'main_address__first_name', 'main_address__last_name', 'main_address__gender', 'main_address__street', 'main_address__postal_code', 'main_address__city', 'main_address__country__name')
    ordering = ('-date_created',)
    filter_horizontal = ()
    inlines = [ca.AddressInline, ca.ImageInline,]

admin.site.register(models.Customer, CustomerAdmin)
