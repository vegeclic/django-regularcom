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
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.contrib.formtools.wizard.views import WizardView, SessionWizardView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from customers import models as cm
from . import forms, models
import products.models as pm
import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week
import numpy as np

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

class SubscriptionUpdateView(generic.UpdateView):
    form_class = forms.SubscriptionUpdateForm
    model = models.Subscription
    template_name = 'carts/subscription_edit.html'
    success_url = '/carts/subscriptions'

    def get_object(self):
        subscription_id = self.kwargs.get('subscription_id')
        return models.Subscription.objects.get(id=subscription_id, customer__account=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, _('Your subscription %d has been updated successfuly.') % self.get_object().id)
        return super(SubscriptionUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SubscriptionUpdateView, self).get_context_data(**kwargs)
        context['section'] = 'cart'
        context['sub_section'] = 'subscriptions'
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SubscriptionUpdateView, self).dispatch(*args, **kwargs)

class DeliveryView(generic.ListView):
    model = models.Delivery
    q = 1.5

    def get_queryset(self):
        subscription_id = self.kwargs.get('subscription_id')
        if subscription_id:
            subscription = models.Subscription.objects.get(id=subscription_id, customer__account=self.request.user)
            deliveries = models.Delivery.objects.filter(subscription=subscription).order_by('date')

            init = subscription.price().price

            k = 0
            last_price = 0
            for delivery in deliveries:
                if delivery.status not in models.Delivery.FAILED_CHOICES:
                    last_price = delivery.payed_price if delivery.payed_price else init/(1+self.q/100)**k
                    k += 1
                delivery.degressive_price = last_price

            return deliveries

        return models.Delivery.objects.filter(subscription__customer__account=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(DeliveryView, self).get_context_data(**kwargs)
        context['section'] = 'cart'
        context['sub_section'] = 'deliveries'
        subscription_id = self.kwargs.get('subscription_id')
        if subscription_id:
            context['subscription'] = models.Subscription.objects.get(id=subscription_id, customer__account=self.request.user)

            deliveries = self.get_queryset()
            init = context['subscription'].price().price

            context['mean_of_prices'] = (np.array([init/(1+self.q/100)**k for k, delivery in enumerate(deliveries.exclude(status__in=models.Delivery.FAILED_CHOICES))]).mean())

        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DeliveryView, self).dispatch(*args, **kwargs)

class DeliveryPaymentView(generic.View):
    def get(self, request, subscription_id, delivery_id):
        subscription = models.Subscription.objects.get(id=subscription_id, customer__account=request.user)
        delivery = models.Delivery.objects.get(id=delivery_id, subscription=subscription)

        if delivery.status != 'w': raise ValueError(_('Delivery %d already payed or canceled.') % delivery.id)

        deliveries = models.Delivery.objects.filter(subscription=subscription, status__in=models.Delivery.SUCCESS_CHOICES)
        delivery.status = 'p'
        delivery.payed_price = subscription.price().price/(1+DeliveryView.q/100)**len(deliveries)
        try:
            delivery.save()
        except ValueError as e:
            messages.error(request, e)
        else:
            messages.success(request, _('The delivery has been successfuly payed.'))
            messages.success(request, _('Your wallet balance has been updated.'))
        return HttpResponseRedirect('/carts/subscriptions/%d/deliveries/' % int(subscription_id))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DeliveryPaymentView, self).dispatch(*args, **kwargs)

class CreateWizard(SessionWizardView):
    template_name = 'carts/create_wizard.html'

    def get_context_data(self, **kwargs):
        context = super(CreateWizard, self).get_context_data(**kwargs)
        context['section'] = 'cart'
        context['sub_section'] = 'create'
        return context

    def get_form(self, step=None, data=None, files=None):
        form = super(CreateWizard, self).get_form(step, data, files)

        # determine the step if not given
        if step is None: step = self.steps.current

        if step == '0':
            form.sizes = models.Size.objects.all()
            form.frequencies = models.FREQUENCY_CHOICES
            form.durations = forms.DURATION_CHOICES
            # cw = Week.withdate(datetime.date.today() + relativedelta(days=10))
            cw = Week.withdate(Week.thisweek().sunday() + relativedelta(days=9))
            form.starts = [str(w + cw.week - 1) for w in Week.weeks_of_year(cw.year)]

            def products_tree(products, root_product=None, root_only=True):
                dict_ = {}
                for product in products:
                    if product == root_product: continue
                    if not product.products_parent.all() or not root_only:
                        dict_[product] = products_tree(product.products_children.all(), root_product=product, root_only=False)
                return dict_

            form.products_tree = products_tree(pm.Product.objects.all())

        elif step == '1':
            form.selected_products = []
            for product in pm.Product.objects.all():
                if int( self.request.POST.get('product_%d' % product.id, 0) ):
                    form.selected_products.append(product)

            cleaned_data = self.get_cleaned_data_for_step('0')
            # if cleaned_data:
            #     form.selected_products = [pm.Product.objects.get(id=product) for product in cleaned_data.get('products')]
            messages.info(self.request, _('In order to lock a product percent, please check the corresponding checkbox.'))

        return form

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]

        products = {}
        for product in pm.Product.objects.all():
            if ('product_%d' % product.id) in form_list[1].data:
                products[product] = int(form_list[1].data['product_%d' % product.id])

        size = models.Size.objects.get(id=form_list[0].data.get('size')[0])

        frequency = int(form_list[0].data.get('frequency'))
        if frequency not in dict(models.FREQUENCY_CHOICES):
            raise ValueError('Frequency doesnot exist.')

        duration = int(form_list[0].data.get('duration'))
        if duration not in dict(forms.DURATION_CHOICES):
            raise ValueError('Duration doesnot exist.')

        bw = Week.fromstring(form_list[0].data.get('start'))
        ew = Week.withdate( bw.day(1) + relativedelta(months=duration) )

        customer = cm.Customer.objects.get(account=self.request.user)

        subscription = models.Subscription.objects.create(customer=customer, size=size, frequency=frequency, start=bw, end=ew)

        for product, extent in products.items():
            subscription.extent_set.create(product=product, extent=extent)

        subscription.create_deliveries()

        messages.success(self.request, _('The subscription was sucessfuly created.'))

        return HttpResponseRedirect('/carts/subscriptions/%d/deliveries/' % subscription.id)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateWizard, self).dispatch(*args, **kwargs)
