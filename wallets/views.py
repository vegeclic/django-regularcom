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

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from . import forms, models

class BalanceView(generic.DetailView):
    model = models.Wallet

    def get_object(self):
        return models.Wallet.objects.get(customer__account=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(BalanceView, self).get_context_data(**kwargs)
        context['section'] = 'wallet'
        context['sub_section'] = 'balance'
        context['balance_in_target_currency'] = self.get_object().balance * self.get_object().target_currency.exchange_rate
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BalanceView, self).dispatch(*args, **kwargs)

class HistoryView(generic.ListView):
    model = models.History

    def get_queryset(self):
        return models.History.objects.filter(wallet__customer__account=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)
        context['section'] = 'wallet'
        context['sub_section'] = 'histories'
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HistoryView, self).dispatch(*args, **kwargs)

class SettingsView(generic.UpdateView):
    form_class = forms.SettingsForm
    model = models.Wallet
    template_name = 'wallets/settings.html'
    success_url = '/wallets'

    def get_object(self):
        return models.Wallet.objects.get(customer__account=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Your settings has been changed successfuly.')
        return super(SettingsView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
        context['section'] = 'wallet'
        context['sub_section'] = 'settings'
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SettingsView, self).dispatch(*args, **kwargs)
