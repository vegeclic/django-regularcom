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
from customers import models as cm
from . import forms, models

class SubscriptionView(generic.ListView):
    model = models.Subscription

    def get_queryset(self):
        return models.Subscription.objects.filter(customer__account=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(SubscriptionView, self).get_context_data(**kwargs)
        context['section'] = 'cart'
        context['sub_section'] = 'subscriptions'
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SubscriptionView, self).dispatch(*args, **kwargs)

class DeliveryView(generic.ListView):
    model = models.Delivery

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return models.Delivery.objects.filter(subscription__id=pk, subscription__customer__account=self.request.user)
        else:
            return models.Delivery.objects.filter(subscription__customer__account=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(DeliveryView, self).get_context_data(**kwargs)
        context['section'] = 'cart'
        context['sub_section'] = 'deliveries'
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DeliveryView, self).dispatch(*args, **kwargs)

class CreateView(generic.CreateView):
    form_class = forms.CreateForm
    model = models.Subscription
    template_name = 'carts/create.html'
    success_url = '/carts/subscriptions'

    def get_object(self):
        return models.Subscription.objects.get(customer__account=self.request.user)

    def form_valid(self, form):
        form.instance.customer = cm.Customer.objects.get(account=self.request.user)
        # messages.success(self.request, 'Your settings has been changed successfuly.')
        return super(CreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['section'] = 'cart'
        context['sub_section'] = 'create'
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateView, self).dispatch(*args, **kwargs)
