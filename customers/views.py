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
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.formtools.wizard.views import WizardView, SessionWizardView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.cache import never_cache, cache_control
from . import forms, models
import common.models as cm
import accounts.models as am
import mailbox.models as mm

class CustomerView(generic.DetailView):
    model = models.Customer

    def get_object(self): return self.request.user.customer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'customers'
        context['sub_section'] = 'profile'
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AddressListView(generic.ListView):
    model = cm.Address
    template_name = 'customers/address_list.html'

    def get_queryset(self): return self.request.user.customer.addresses.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'customers'
        context['sub_section'] = 'addresses'
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AddressCreateView(generic.CreateView):
    form_class = forms.AddressCreateForm
    model = cm.Address
    template_name = 'customers/address_create.html'
    success_url = reverse_lazy('addresses')

    def get_object(self): return self.request.user.customer

    def form_valid(self, form):
        fi = form.instance
        fi.content_type = ContentType.objects.get(model='customer')
        fi.object_id = self.request.user.customer.id
        messages.success(self.request, _('Your new address has been well created.'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'customers'
        context['sub_section'] = 'address_create'
        context['object'] = self.get_object()
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AddressDeleteView(generic.DeleteView):
    model = cm.Address
    template_name = 'customers/address_confirm_delete.html'
    # success_url = reverse_lazy('addresses') # raise an exception
    success_url = '/customers/addresses'

    def get_object(self):
        return self.request.user.customer.addresses.get(id=self.kwargs.get('address_id'))

    def get_success_url(self):
        messages.success(self.request, _('Your address has been well deleted.'))
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'customers'
        context['sub_section'] = 'addresses'
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AddressUpdateView(generic.UpdateView):
    form_class = forms.AddressUpdateForm
    model = cm.Address
    template_name = 'customers/address_edit.html'
    # success_url = '/customers/addresses'
    success_url = reverse_lazy('addresses')

    def get_object(self):
        return self.request.user.customer.addresses.get(id=self.kwargs.get('address_id'))

    def form_valid(self, form):
        messages.success(self.request, _('Your address %d has been updated successfuly.') % self.get_object().id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'customers'
        context['sub_section'] = 'addresses'
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AddressDefineAsMainView(generic.View):
    def get(self, request, address_id):
        customer = self.request.user.customer
        address = customer.addresses.get(id=address_id)
        customer.main_address = address
        customer.save()
        messages.success(request, _('The address %s has been defined as main address.') % address.__unicode__())
        return HttpResponseRedirect('/customers/addresses/')

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AddressDefineAsShippingView(generic.View):
    def get(self, request, address_id):
        customer = self.request.user.customer
        address = customer.addresses.get(id=address_id)
        customer.shipping_address = address
        customer.save()
        messages.success(request, _('The address %s has been defined as shipping address.') % address.__unicode__())
        return HttpResponseRedirect('/customers/addresses/')

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AddressDefineAsBillingView(generic.View):
    def get(self, request, address_id):
        customer = self.request.user.customer
        address = customer.addresses.get(id=address_id)
        customer.billing_address = address
        customer.save()
        messages.success(request, _('The address %s has been defined as billing address.') % address.__unicode__())
        return HttpResponseRedirect('/customers/addresses/')

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class AddressDefineAsRelayView(generic.View):
    def get(self, request, address_id):
        customer = self.request.user.customer
        address = customer.addresses.get(id=address_id)
        customer.relay_address = address
        customer.save()
        messages.success(request, _('The address %s has been defined as relay address.') % address.__unicode__())
        return HttpResponseRedirect('/customers/addresses/')

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class PasswordResetView(generic.View):
    def get(self, request):
        account = self.request.user
        password = am.Account.objects.make_random_password()
        account.set_password(password)
        account.save()
        customer = self.request.user.customer

        mm.Message.objects.create_message(mail_only=True, participants=[customer], subject=_('Password reset'), body=_(
"""Hi %(name)s,

A request to reset your password was made with your account %(email)s from the website of Végéclic.

You will find your new password below:

New password: %(password)s

Best regards,
Végéclic.
"""
            ) % {'name': customer.main_address.__unicode__(), 'email': account.email, 'password': password})

        messages.success(request, _('The password has been regenerated. You will receive an email with the new password.'))

        return HttpResponseRedirect('/customers/')

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class SettingsView(generic.UpdateView):
    form_class = forms.SettingsForm
    model = am.Account
    template_name = 'customers/settings.html'
    success_url = '/customers'

    def get_object(self): return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Your settings has been changed successfuly.'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'customers'
        context['sub_section'] = 'settings'
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
