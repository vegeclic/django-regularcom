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
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError
from . import models, forms
import common.admin as ca
import common.models as cm

class WalletAdmin(ca.MyModelAdmin):
    form = forms.WalletAdminForm
    list_display = ('customer', 'balance', 'balance_in_target_currency', 'target_currency',)
    list_filter = ('target_currency',)

admin.site.register(models.Wallet, WalletAdmin)

class CreditAdmin(ca.MyModelAdmin):
    add_form = forms.CreditCreationAdminForm
    form = forms.CreditAdminForm
    list_display = ('wallet', 'payment_type', 'amount', 'currency', 'payment_date', 'date_created', 'status',)
    list_filter = ('status', 'wallet', 'payment_type', 'currency',)
    # readonly_fields = ('status',)
    # fieldsets = (
    #     (None, {'fields': ('status', 'wallet', 'payment_type', 'amount', 'currency',)}),
    #     (_('Differ'), {'classes': ('collapse',), 'fields': ('payment_date',)}),
    # )
    search_fields = ['wallet__customer__account__email']
    actions = ['make_draft', 'make_validated', 'make_expired', 'make_withdrawn',]

    def change_status(self, request, queryset, status):
        for c in queryset:
            if c.status == 'v': continue
            c.status = status
            c.save()

    def make_draft(self, request, queryset): self.change_status(request, queryset, 'd')
    def make_validated(self, request, queryset): self.change_status(request, queryset, 'v')
    def make_expired(self, request, queryset): self.change_status(request, queryset, 'e')
    def make_withdrawn(self, request, queryset): self.change_status(request, queryset, 'w')

admin.site.register(models.Credit, CreditAdmin)

class WithdrawAdmin(ca.MyModelAdmin):
    add_form = forms.WithdrawCreationAdminForm
    form = forms.WithdrawAdminForm
    list_display = ('wallet', 'payment_type', 'amount', 'currency', 'date_created', 'status',)
    list_filter = ('status', 'wallet', 'payment_type', 'currency',)
    search_fields = ['wallet__customer__account__email']
    actions = ['make_draft', 'make_validated', 'make_expired', 'make_withdrawn',]

    def change_status(self, request, queryset, status):
        for c in queryset:
            if c.status == 'v': continue
            c.status = status
            c.save()

    def make_draft(self, request, queryset): self.change_status(request, queryset, 'd')
    def make_validated(self, request, queryset): self.change_status(request, queryset, 'v')
    def make_expired(self, request, queryset): self.change_status(request, queryset, 'e')
    def make_withdrawn(self, request, queryset): self.change_status(request, queryset, 'w')

admin.site.register(models.Withdraw, WithdrawAdmin)

class HistoryAdmin(ca.MyModelAdmin):
    add_form = forms.HistoryCreationAdminForm
    form = forms.HistoryAdminForm
    list_display = ('wallet', 'content_type', 'value', 'amount', 'wallet_amount', 'target_currency', 'date_created',)
    list_filter = ('wallet', 'content_type',)

    def value(self, obj): return obj.content_object

    def wallet_amount(self, obj):
        return obj.amount * obj.wallet.target_currency.exchange_rate

    def target_currency(self, obj): return obj.wallet.target_currency

admin.site.register(models.History, HistoryAdmin)
