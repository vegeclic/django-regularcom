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
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.cache import never_cache, cache_control
from . import forms, models

class BalanceView(generic.DetailView):
    model = models.Wallet

    def get_object(self):
        return models.Wallet.objects.get(customer__account=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'wallet'
        context['sub_section'] = 'balance'
        context['balance_in_target_currency'] = self.get_object().balance * self.get_object().target_currency.exchange_rate
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class HistoryView(generic.ListView):
    model = models.History

    def get_queryset(self):
        return models.History.objects.filter(wallet__customer__account=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'wallet'
        context['sub_section'] = 'histories'
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class CreditRequestView(generic.ListView):
    model = models.Credit

    def get_queryset(self):
        return models.Credit.objects.filter(wallet__customer__account=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'wallet'
        context['sub_section'] = 'credit_requests'
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class WithdrawRequestView(generic.ListView):
    model = models.Withdraw

    def get_queryset(self):
        return models.Withdraw.objects.filter(wallet__customer__account=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'wallet'
        context['sub_section'] = 'withdraw_requests'
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class CreditView(generic.CreateView):
    form_class = forms.CreditForm
    model = models.Credit
    template_name = 'wallets/credit.html'
    success_url = '/wallets'

    def get_object(self):
        return models.Wallet.objects.get(customer__account=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, _('Your credit request has been sent successfuly. You will be noticed about its validation as soon as possible. If you made any mistakes, it is still possible to undo (see Credit histories).'))
        fi = form.instance
        fi.wallet = self.get_object()
        fi.currency = self.get_object().target_currency
        fi.amount = abs(round(fi.amount/fi.currency.exchange_rate,2))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'wallet'
        context['sub_section'] = 'credit'
        context['object'] = self.get_object()
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class WithdrawView(generic.CreateView):
    form_class = forms.WithdrawForm
    model = models.Withdraw
    template_name = 'wallets/withdraw.html'
    success_url = '/wallets'

    def get_object(self):
        return models.Wallet.objects.get(customer__account=self.request.user)

    def form_valid(self, form):
        form.instance.wallet = self.get_object()
        form.instance.currency = self.get_object().target_currency
        try:
            response = super().form_valid(form)
            messages.success(self.request, _('Your withdraw request has been sent successfuly. You will be noticed about its validation as soon as possible. If you made any mistakes, it is still possible to undo (see Withdraw histories).'))
            return response
        except ValueError as e:
            messages.error(self.request, e)
            return HttpResponseRedirect('/wallets/withdraw/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'wallet'
        context['sub_section'] = 'withdraw'
        context['object'] = self.get_object()
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class WithdrawCancelView(generic.View):
    def get(self, request, withdraw_id):
        withdraw = models.Withdraw.objects.get(id=withdraw_id, wallet__customer__account=request.user)
        withdraw.status = 'c'
        try:
            withdraw.save()
        except ValueError as e:
            messages.error(request, e)
        else:
            messages.success(request, _('The withdraw request has been canceled.'))
            messages.success(request, _('Your wallet balance has been updated.'))
        return HttpResponseRedirect('/wallets/withdraw_requests/')

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class CreditCancelView(generic.View):
    def get(self, request, credit_id):
        credit = models.Credit.objects.get(id=credit_id, wallet__customer__account=request.user)
        credit.status = 'c'
        try:
            credit.save()
        except ValueError as e:
            messages.error(request, e)
        else:
            messages.success(request, _('The credit request has been canceled.'))
        return HttpResponseRedirect('/wallets/credit_requests/')

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class SettingsView(generic.UpdateView):
    form_class = forms.SettingsForm
    model = models.Wallet
    template_name = 'wallets/settings.html'
    success_url = '/wallets'

    def get_object(self):
        return models.Wallet.objects.get(customer__account=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, _('Your settings has been changed successfuly.'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'wallet'
        context['sub_section'] = 'settings'
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
