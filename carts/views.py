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

from django.conf import settings
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.contrib.formtools.wizard.views import WizardView, SessionWizardView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.views.decorators.cache import never_cache, cache_control
from customers import models as cm
from . import forms, models
import products.models as pm
import mailbox.models as mm
import suppliers.views as sw
import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week
import numpy as np

class ThematicListView(generic.ListView):
    model = models.Thematic
    template_name = 'carts/thematic_list.html'

    def get_queryset(self):
        object_list = cache.get('thematic_list') or self.model.objects.language('fr').select_related('main_image').order_by('name').all()
        if not cache.get('thematic_list'): cache.set('thematic_list', object_list)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'cart'
        context['sub_section'] = 'create_thematic'
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs): return super().dispatch(*args, **kwargs)

class SubscriptionView(generic.ListView):
    model = models.Subscription
    template_name = 'carts/subscription_list.html'

    def get_queryset(self):
        subscriptions = self.model.objects.select_related().filter(customer__account=self.request.user)

        paginator = Paginator(subscriptions, 10)

        page = self.kwargs.get('page', 1)
        try:
            subscriptions_per_page = paginator.page(page)
        except PageNotAnInteger:
            subscriptions_per_page = paginator.page(1)
        except EmptyPage:
            subscriptions_per_page = paginator.page(paginator.num_pages)

        return subscriptions_per_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'cart'
        context['sub_section'] = 'subscriptions'
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs): return super().dispatch(*args, **kwargs)

class SubscriptionUpdateView(generic.UpdateView):
    form_class = forms.SubscriptionUpdateForm
    model = models.Subscription
    template_name = 'carts/subscription_edit.html'
    success_url = '/carts/subscriptions/page/1'

    def get_object(self):
        subscription_id = self.kwargs.get('subscription_id')
        return self.model.objects.get(id=subscription_id, customer__account=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, _('Your subscription %d has been updated successfuly.') % self.get_object().id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'cart'
        context['sub_section'] = 'subscriptions'
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs): return super().dispatch(*args, **kwargs)

class DeliveryView(generic.ListView):
    model = models.Delivery
    template_name = 'carts/delivery_list.html'

    def get_queryset(self):
        deliveries = self.model.objects.filter(subscription__customer__account=self.request.user).select_related().order_by('date')

        subscription_id = self.kwargs.get('subscription_id')
        if subscription_id: deliveries = deliveries.filter(subscription__id=subscription_id)

        deliveries = deliveries.all()

        if subscription_id and deliveries:
            init = deliveries[0].subscription.price().price
            k = 0
            last_price = 0
            for delivery in deliveries:
                if delivery.status not in self.model.FAILED_CHOICES:
                    last_price = delivery.payed_price if delivery.payed_price else init/(1+settings.DEGRESSIVE_PRICE_RATE/100)**k
                    k += 1
                delivery.degressive_price = last_price

        paginator = Paginator(deliveries, 10)

        page = self.kwargs.get('page', 1)
        try:
            deliveries_per_page = paginator.page(page)
        except PageNotAnInteger:
            deliveries_per_page = paginator.page(1)
        except EmptyPage:
            deliveries_per_page = paginator.page(paginator.num_pages)

        return deliveries_per_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'cart'
        context['sub_section'] = 'deliveries'
        subscription_id = self.kwargs.get('subscription_id')
        if subscription_id:
            context['subscription'] = models.Subscription.objects.select_related().get(id=subscription_id, customer__account=self.request.user)

            deliveries = self.model.objects.filter(subscription=context['subscription']).select_related().order_by('date')
            init = context['subscription'].price().price

            context['mean_of_prices'] = (np.array([init/(1+settings.DEGRESSIVE_PRICE_RATE/100)**k for k, delivery in enumerate(deliveries.exclude(status__in=self.model.FAILED_CHOICES))]).mean())

        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs): return super().dispatch(*args, **kwargs)

class DeliveryPaymentView(generic.View):
    def get(self, request, subscription_id, delivery_id):
        subscription = models.Subscription.objects.get(id=subscription_id, customer__account=request.user)
        delivery = models.Delivery.objects.get(id=delivery_id, subscription=subscription)

        if delivery.status != 'w': raise ValueError(_('Delivery %d already payed or canceled.') % delivery.id)

        deliveries = models.Delivery.objects.filter(subscription=subscription, status__in=models.Delivery.SUCCESS_CHOICES)
        delivery.status = 'p'
        delivery.payed_price = subscription.price().price/(1+settings.DEGRESSIVE_PRICE_RATE/100)**len(deliveries)
        try:
            delivery.save()
        except ValueError as e:
            messages.error(request, e)
        else:
            messages.success(request, _('The delivery has been successfuly payed.'))
            messages.success(request, _('Your wallet balance has been updated.'))
        return HttpResponseRedirect('/carts/subscriptions/%d/deliveries/' % int(subscription_id))

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs): return super().dispatch(*args, **kwargs)

def show_extent_form_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('customized', True)

class CreateWizard(SessionWizardView):
    template_name = 'carts/create_wizard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'cart'
        thematic_id = self.kwargs.get('thematic_id')
        if thematic_id:
            context['sub_section'] = 'create_thematic'
            context['thematic'] = models.Thematic.objects.select_related().get(id=thematic_id)
        else:
            context['sub_section'] = 'create_custom'
        return context

    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)

        # determine the step if not given
        if step is None: step = self.steps.current

        try:
            thematic = models.Thematic.objects.select_related().get(id=self.kwargs.get('thematic_id', None))
        except models.Thematic.DoesNotExist:
            thematic = None

        thematic_products = [e.product for e in thematic.thematicextent_set.all()] if thematic else []
        form.thematic_products = thematic_products

        if step == '0':
            if thematic:
                for k, f in [('size', thematic.size),
                             ('carrier', thematic.carrier),
                             ('frequency', thematic.frequency),
                             ('start', thematic.start_duration)]:
                    if f: form.fields[k].initial = f

                if thematic.end_duration:
                    delta = relativedelta(Week.fromstring(thematic.end_duration).day(1),
                                          Week.fromstring(thematic.start_duration).day(1))
                    form.fields['duration'].initial = delta.months

                for field, locked in [('size', thematic.locked_size),
                                      ('carrier', thematic.locked_carrier),
                                      ('receive_only_once', thematic.locked_receive_only_once),
                                      ('frequency', thematic.locked_frequency),
                                      ('start', thematic.locked_start),
                                      ('duration', thematic.locked_duration),
                                      ('criterias', thematic.locked_criterias)]:
                    if locked:
                        form.fields[field].widget.attrs['class'] = form.fields[field].widget.attrs.get('class', '') + ' disabled'

                if thematic.criterias:
                    form.fields['criterias'].initial = [v.id for v in thematic.criterias.all()]

            form.products_tree = cache.get('products_tree') or sw.get_products_tree(pm.Product.objects)
            if not cache.get('products_tree'): cache.set('products_tree', form.products_tree)

            form.carriers = cache.get('create_carriers') or models.Carrier.objects.select_related().all()
            if not cache.get('create_carriers'): cache.set('create_carriers', form.carriers)

            form.sizes = cache.get('create_sizes') or models.Size.objects.select_related().all()
            if not cache.get('create_sizes'): cache.set('create_sizes', form.sizes)

            if not thematic: form.fields['customized'].initial = True

        elif step == '1':
            products = []
            for product in pm.Product.objects.language('fr').order_by('name').all():
                if int( self.request.POST.get('product_%d' % product.id, 0) ):
                    products.append(product)

            if not products:
                raise forms.forms.ValidationError("no product was selected")

            extents = [e.extent for e in thematic.thematicextent_set.all()] if thematic else []
            shared_extent = int((100 - sum(extents))/(len(products) - len(extents))) if (len(products) - len(extents)) else 0

            form.selected_products = []
            for product in products:
                extent = None
                if product in thematic_products:
                    extent = thematic.thematicextent_set.get(product=product)
                form.selected_products.append((product, extent.extent if extent else shared_extent))

            messages.info(self.request, _('In order to lock a product percent, please check the corresponding checkbox.'))

        return form

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]
        customized = form_data[0].get('customized', False)

        try:
            thematic = models.Thematic.objects.select_related().get(id=self.kwargs.get('thematic_id', None))
        except models.Thematic.DoesNotExist:
            thematic = None

        thematic_products = [e.product for e in thematic.thematicextent_set.all()] if thematic else []

        products = {}
        if customized:
            for product in pm.Product.objects.select_related().all():
                if ('product_%d' % product.id) in form_list[1].data:
                    products[product] = int(form_list[1].data['product_%d' % product.id])
        else:
            if thematic:
                for e in thematic.thematicextent_set.all():
                    products[e.product] = e.extent

        if not products:
            raise forms.forms.ValidationError("no product was selected")

        size = form_data[0].get('size')
        carrier = form_data[0].get('carrier')
        receive_only_once = form_data[0].get('receive_only_once', False)
        frequency = int(form_data[0].get('frequency'))
        duration = int(form_data[0].get('duration'))
        bw = Week.fromstring(form_data[0].get('start'))
        ew = Week.withdate( bw.day(1) + relativedelta(months=duration) )
        customer = self.request.user.customer
        criterias = form_data[0].get('criterias')

        subscription = models.Subscription.objects.create(customer=customer, size=size, carrier=carrier, receive_only_once=receive_only_once, frequency=frequency, start=bw, end=ew)

        subscription.criterias = criterias

        for product, extent in products.items():
            subscription.extent_set.create(product=product, extent=extent)
        subscription.create_deliveries()

        messages.success(self.request, _('The subscription was sucessfuly created.'))

        deliveries = subscription.delivery_set.order_by('date')

        mm.Message.objects.create_message(participants=[customer], subject=_('Votre abonnement %(subscription_id)d a été crée') % {'subscription_id': subscription.id}, body=_(
"""Bonjour %(name)s,

Nous sommes heureux de vous annoncer que votre abonnement %(subscription_id)d a été crée, il est accessible à l'adresse suivante :

http://www.vegeclic.fr/carts/subscriptions/%(subscription_id)d/deliveries/

Vous êtes invité, à présent, à approvisionner votre portemonnaie vers un solde suffisant afin que l'on valide la première échéance du %(date)s de votre abonnement en cliquant sur le lien suivant :

http://www.vegeclic.fr/wallets/credit/

Si ce n'est pas encore fait, merci de bien vouloir renseigner vos cordonnées à cette adresse :

http://www.vegeclic.fr/customers/addresses/create/

Bien cordialement,
Végéclic.
"""
        ) % {'name': customer.main_address.__unicode__() if customer.main_address else '', 'date': deliveries[0].get_date_display(), 'subscription_id': subscription.id})

        return HttpResponseRedirect('/carts/subscriptions/%d/deliveries/page/1' % subscription.id)

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs): return super().dispatch(*args, **kwargs)

CREATEALL_TEMPLATES = {
    'cart': 'carts/create_all/cart.html',
    'subscription': 'carts/create_all/subscription.html',
    'products': 'carts/create_all/products.html',
    'extents': 'carts/create_all/extents.html',
    'suppliers': 'carts/create_all/suppliers.html',
    'preview': 'carts/create_all/preview.html',
    'authentication': 'carts/create_all/authentication.html',
    'payment': 'carts/create_all/payment.html',
    'address': 'carts/create_all/address.html',
    'comment': 'carts/create_all/comment.html',
    'resume': 'carts/create_all/resume.html',
    'validation': 'carts/create_all/validation.html',
}

class CreateAllCartStep:
    def __call__(self, view=None, form=None, step=None, data=None, files=None):
        form.thematic_list = cache.get('thematic_list') or models.Thematic.objects.language('fr').select_related('main_image').order_by('name').all()
        if not cache.get('thematic_list'): cache.set('thematic_list', form.thematic_list)
        return form

def get_thematic(wizard):
    cart_data = wizard.get_cleaned_data_for_step('cart') or {}
    try:
        thematic = models.Thematic.objects.select_related().get(id=cart_data.get('choice', None))
    except models.Thematic.DoesNotExist:
        thematic = None
    except ValueError:
        thematic = None
    return thematic

class CreateAllSubscriptionStep:
    def __call__(self, wizard=None, form=None, step=None, data=None, files=None):
        cart_data = wizard.get_cleaned_data_for_step('cart') or {}

        form.thematic = get_thematic(wizard)

        if form.thematic:
            for k, f in [('size', form.thematic.size),
                         ('carrier', form.thematic.carrier),
                         ('frequency', form.thematic.frequency),
                         ('start', form.thematic.start_duration)]:
                if f: form.fields[k].initial = f

            if form.thematic.end_duration:
                delta = relativedelta(Week.fromstring(form.thematic.end_duration).day(1),
                                      Week.fromstring(form.thematic.start_duration).day(1))
                form.fields['duration'].initial = delta.months

            for field, locked in [('size', form.thematic.locked_size),
                                  ('carrier', form.thematic.locked_carrier),
                                  ('receive_only_once', form.thematic.locked_receive_only_once),
                                  ('frequency', form.thematic.locked_frequency),
                                  ('start', form.thematic.locked_start),
                                  ('duration', form.thematic.locked_duration),
                                  ('criterias', form.thematic.locked_criterias)]:
                if locked:
                    form.fields[field].widget.attrs['class'] = form.fields[field].widget.attrs.get('class', '') + ' disabled'

            if form.thematic.criterias:
                form.fields['criterias'].initial = [v.id for v in form.thematic.criterias.all()]

            form.fields['receive_only_once'].initial = form.thematic.receive_only_once
            form.fields['customized'].initial = False

        form.carriers = cache.get('create_carriers') or models.Carrier.objects.select_related().all()
        if not cache.get('create_carriers'): cache.set('create_carriers', form.carriers)

        form.sizes = cache.get('create_sizes') or models.Size.objects.select_related().all()
        if not cache.get('create_sizes'): cache.set('create_sizes', form.sizes)

        return form

class CreateAllProductsStep:
    def __call__(self, wizard=None, form=None, step=None, data=None, files=None):
        form.thematic = get_thematic(wizard)
        return form

class CreateAllExtentsStep:
    def __call__(self, wizard=None, form=None, step=None, data=None, files=None):
        return form

class CreateAllSuppliersStep:
    def __call__(self, wizard=None, form=None, step=None, data=None, files=None):
        return form

class CreateAllPreviewStep:
    def __call__(self, wizard=None, form=None, step=None, data=None, files=None):
        return form

class CreateAllAuthenticationStep:
    def __call__(self, wizard=None, form=None, step=None, data=None, files=None):
        return form

class CreateAllPaymentStep:
    def __call__(self, wizard=None, form=None, step=None, data=None, files=None):
        return form

class CreateAllAddressStep:
    def __call__(self, wizard=None, form=None, step=None, data=None, files=None):
        return form

class CreateAllCommentStep:
    def __call__(self, wizard=None, form=None, step=None, data=None, files=None):
        return form

class CreateAllResumeStep:
    def __call__(self, wizard=None, form=None, step=None, data=None, files=None):
        return form

class CreateAllValidationStep:
    def __call__(self, wizard=None, form=None, step=None, data=None, files=None):
        return form

CREATEALL_STEPS = {
    'cart': CreateAllCartStep(),
    'subscription': CreateAllSubscriptionStep(),
    'products': CreateAllProductsStep(),
    'extents': CreateAllExtentsStep(),
    'suppliers': CreateAllSuppliersStep(),
    'preview': CreateAllPreviewStep(),
    'authentication': CreateAllAuthenticationStep(),
    'payment': CreateAllPaymentStep(),
    'address': CreateAllAddressStep(),
    'comment': CreateAllCommentStep(),
    'resume': CreateAllResumeStep(),
    'validation': CreateAllValidationStep(),
}

CREATEALL_STEPS_ORDER = ['cart', 'subscription', 'products', 'extents', 'suppliers', 'preview', 'authentication', 'payment', 'address', 'comment', 'resume', 'validation',]

def show_create_all_products_form_condition(wizard):
    subscription_data = wizard.get_cleaned_data_for_step('subscription') or {}
    return subscription_data.get('customized', False)

class CreateAll(SessionWizardView):
    def get_template_names(self): return [CREATEALL_TEMPLATES[self.steps.current]]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'cart'
        context['sub_section'] = 'create_all'
        return context

    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)
        if step is None: step = self.steps.current

        step_idx = CREATEALL_STEPS_ORDER.index(step)
        count = len(CREATEALL_STEPS_ORDER)

        form.progress_value = 0
        form.current_progress_value = 0
        if step == 'cart':
            form.progress_value = 0
        elif step == 'validation':
            form.progress_value = 100
        else:
            form.progress_value = int(step_idx/count*100)
            form.current_progress_value = int(1/count*100)
        form.inverse_progress_value = 100-(form.progress_value + form.current_progress_value)

        return CREATEALL_STEPS[step](self, form, step, data, files)

    def process_step(self, form):
        print(self.get_all_cleaned_data())
        return super().process_step(form)

    def done(self, form_list, **kwargs):
        form_data = dict(zip(CREATEALL_STEPS_ORDER, [form.cleaned_data for form in form_list]))
        print(form_data)
        raise ValueError('done')
        # return HttpResponseRedirect('/carts/create/all')

    # @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs): return super().dispatch(*args, **kwargs)
