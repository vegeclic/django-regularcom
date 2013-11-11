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
import django.contrib.auth as auth
import customers.models as cm
from . import forms, models
import products.models as pm
import suppliers.models as sm
import mailbox.models as mm
import suppliers.views as sw
import accounts.models as am
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
    # 'validation': 'carts/create_all/validation.html',
}

# CreateAll base classes

class CreateAllStep:
    def __call__(self, wizard, form, step, data, files): return form

class CreateAllProcessStep:
    def __call__(self, wizard, form): return form

class CreateAllDone:
    def __call__(self, wizard, own_data, form_data, tmp_dict): return True

# end of base classes

def get_user(wizard):
    user = None
    if wizard.request.user.is_authenticated():
        user = wizard.request.user
    else:
        user = wizard.storage.extra_data.get('user', None)
    return user

def get_thematic(wizard):
    cart_data = wizard.get_cleaned_data_for_step('cart') or {}
    try:
        thematic = models.Thematic.objects.select_related().get(id=cart_data.get('choice', None))
    except models.Thematic.DoesNotExist:
        thematic = None
    except ValueError:
        thematic = None
    return thematic

def get_thematic_done(form_data):
    cart_data = form_data.get('cart') or {}
    try:
        thematic = models.Thematic.objects.select_related().get(id=cart_data.get('choice', None))
    except models.Thematic.DoesNotExist:
        thematic = None
    except ValueError:
        thematic = None
    return thematic

class CreateAllCartStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        form.thematic_list = cache.get('thematic_list') or models.Thematic.objects.language('fr').select_related('main_image').order_by('name').all()
        if not cache.get('thematic_list'): cache.set('thematic_list', form.thematic_list)
        return form

class CreateAllSubscriptionStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
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
                    attrs = form.fields[field].widget.attrs
                    attrs['class'] = attrs.get('class', '') + ' disabled'

            if form.thematic.criterias:
                form.fields['criterias'].initial = [v.id for v in form.thematic.criterias.all()]

            form.fields['receive_only_once'].initial = form.thematic.receive_only_once
            form.fields['customized'].initial = False
        else:
            form.fields['customized'].initial = True
            attrs = form.fields['customized'].widget.attrs
            attrs['class'] = attrs.get('class', '') + ' disabled'

        form.carriers = cache.get('create_carriers') or models.Carrier.objects.select_related().all()
        if not cache.get('create_carriers'): cache.set('create_carriers', form.carriers)

        form.sizes = cache.get('create_sizes') or models.Size.objects.select_related().all()
        if not cache.get('create_sizes'): cache.set('create_sizes', form.sizes)

        return form

class CreateAllSubscriptionDone(CreateAllDone):
    def __call__(self, wizard, own_data, form_data, tmp_dict):
        print('subscription done')

        print(tmp_dict)

        user = get_user(wizard)
        thematic = get_thematic_done(form_data)
        customized = own_data.get('customized', False)
        __customized = form_data['cart'].get('choice', 'perso') == 'perso' or own_data.get('customized', False)

        duration = int(own_data.get('duration'))
        bw = Week.fromstring(own_data.get('start'))
        ew = Week.withdate( bw.day(1) + relativedelta(months=duration) )

        subscription = models.Subscription.objects.create(customer=user.customer, size=own_data['size'], carrier=own_data['carrier'], receive_only_once=own_data['receive_only_once'], frequency=int(own_data['frequency']), start=bw, end=ew)

        subscription.criterias = own_data['criterias']

        if thematic and not customized:
            for e in thematic.thematicextent_set.all():
                subscription.extent_set.create(product=e.product, extent=e.extent, customized=False)

        subscription.create_deliveries()

        tmp_dict['subscription'] = subscription

        return True

class CreateAllProductsStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        form.thematic = get_thematic(wizard)
        form.thematic_products = [e.product for e in form.thematic.thematicextent_set.all()] if form.thematic else []

        form.modified = True if data else False

        form.products_tree = cache.get('products_tree') or sw.get_products_tree(pm.Product.objects)
        if not cache.get('products_tree'): cache.set('products_tree', form.products_tree)

        return form

class CreateAllProductsDone(CreateAllDone):
    def __call__(self, wizard, own_data, form_data, tmp_dict):
        subscription = tmp_dict['subscription']

        print('products', subscription)

        products_data = form_data.get('products') or {}
        extents_data = form_data.get('extents') or {}

        products = products_data.get('products', [])

        for product in products:
            extent = extents_data.get('product_%d' % product.id, 0)
            custom = extents_data.get('choice_supplier_product_%d' % product.id, 'false') == 'true'
            subscription.extent_set.create(product=product, extent=extent, customized=custom)

        return True

class CreateAllExtentsStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        products_data = wizard.get_cleaned_data_for_step('products') or {}
        form.thematic = get_thematic(wizard)

        products = products_data.get('products', [])
        thematic_products = [e.product for e in form.thematic.thematicextent_set.all()] if form.thematic else []

        extents = [e.extent for e in form.thematic.thematicextent_set.all()] if form.thematic else []
        shared_extent = int((100 - sum(extents))/(len(products) - len(extents))) if (len(products) - len(extents)) else 0

        for product in products:
            extent = form.thematic.thematicextent_set.get(product=product) if product in thematic_products else None
            form.fields['product_%d' % product.id] = f1 = forms.forms.IntegerField(widget=forms.forms.HiddenInput, label=product.name, initial=extent.extent if extent else shared_extent, min_value=0, max_value=100)
            form.fields['choice_supplier_product_%d' % product.id] = f2 = forms.forms.ChoiceField(widget=forms.forms.RadioSelect(renderer=forms.MyRadioFieldRenderer), label='boolean')
            f2.choices = [('false', _('Je laisse Végéclic choisir')), ('true', _('Je souhaite choisir'))]
            f2.initial = 'false'
            f1.widget.attrs['class'] = 'input_value'

        return form

class CreateAllSuppliersStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        subscription_data = wizard.get_cleaned_data_for_step('subscription') or {}
        products_data = wizard.get_cleaned_data_for_step('products') or {}
        extents_data = wizard.get_cleaned_data_for_step('extents') or {}

        size = subscription_data.get('size', None)
        products = products_data.get('products', [])

        products_tree = cache.get('products_tree') or sw.get_products_tree(pm.Product.objects)
        if not cache.get('products_tree'): cache.set('products_tree', products_tree)

        for product in products:
            if extents_data.get('choice_supplier_product_%d' % product.id, 'false') == 'false': continue
            price = size.default_price().price*extents_data.get('product_%d' % product.id, 1)/100
            print(price)
            root = sw.find_product(products_tree, product.id)
            qs = sm.Product.objects.language('fr').filter(status='p', product__in=sw.products_tree_to_list(root)).select_related('price', 'main_image', 'price__currency', 'price__tax').prefetch_related('criterias', 'suppliers').order_by('-date_created')
            form.fields['supplier_product_%d' % product.id] = f = forms.forms.ModelMultipleChoiceField(widget=forms.MyImageCheckboxSelectMultiple, queryset=qs, label=product.name)
            supplier_products_list = qs.all()
            f.choices = [(p.id, '%s|%s|%s' % (p.name, p.main_image.image, p.price().get_after_tax_price()/price*100)) for p in supplier_products_list]

        return form

class CreateAllPreviewStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):

        return form

class CreateAllAuthenticationStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        form.user = wizard.storage.extra_data.get('user', None)
        return form

class CreateAllAuthenticationProcessStep(CreateAllProcessStep):
    def __call__(self, wizard, form):
        if not form.cleaned_data: return form
        if wizard.storage.extra_data.get('user', None): return form

        email = form.cleaned_data.get('email').lower()

        if form.cleaned_data.get('sign_type') == 'up':
            wizard.storage.extra_data['user'] = user = am.Account.objects.create_user(email=email)
            messages.success(wizard.request, _("Your account has been successfully created."))
            return form

        # sign in
        password = form.cleaned_data.get('password')
        user = auth.authenticate(username=email, password=password)
        if user is None: raise forms.forms.ValidationError(_('bad credentials'))
        wizard.storage.extra_data['user'] = user
        # auth.login(wizard.request, user)
        messages.success(wizard.request, _("You're logged in."))
        return form

class CreateAllPaymentStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        subscription_data = wizard.get_cleaned_data_for_step('subscription') or {}
        size = subscription_data.get('size', None)

        if size:
            form.price = size.default_price()

        user = get_user(wizard)
        if user:
            form.balance = user.customer.wallet.balance_in_target_currency()
            form.currency = user.customer.wallet.target_currency

        return form

class CreateAllAddressStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        user = get_user(wizard)
        if user:
            if user.customer.main_address:
                address = user.customer.main_address
                for k, f in [('first_name', address.first_name), ('last_name', address.last_name),
                             ('street', address.street), ('postal_code', address.postal_code),
                             ('city', address.city), ('country', address.country),
                             ('home_phone', address.home_phone), ('mobile_phone', address.mobile_phone)]:
                    form.fields[k].initial = f

            if user.customer.relay_address:
                relay = user.customer.main_address
                for k, f in [('relay_name', relay.first_name), ('relay_street', relay.street),
                             ('relay_postal_code', relay.postal_code), ('relay_city', relay.city)]:
                    form.fields[k].initial = f

        return form

class CreateAllCommentStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        return form

class CreateAllResumeStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        return form

class CreateAllValidationStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
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
    # 'validation': CreateAllValidationStep(),
}

CREATEALL_PROCESS_STEPS = {
    'authentication': CreateAllAuthenticationProcessStep(),
}

CREATEALL_DONE = {
    'subscription': CreateAllSubscriptionDone(),
    'products': CreateAllProductsDone(),
}

# CREATEALL_STEPS_ORDER = ['cart', 'subscription', 'products', 'extents', 'suppliers', 'preview', 'authentication', 'payment', 'address', 'comment', 'resume', 'validation',]
CREATEALL_STEPS_ORDER = ['cart', 'subscription', 'products', 'extents', 'suppliers', 'preview', 'authentication', 'payment', 'address', 'comment', 'resume',]

CREATEALL_FORMS = [
    ('cart', forms.CreateAllCartForm),
    ('subscription', forms.CreateAllSubscriptionForm),
    ('products', forms.CreateAllProductsForm),
    ('extents', forms.CreateAllExtentsForm),
    ('suppliers', forms.CreateAllSuppliersForm),
    ('preview', forms.CreateAllPreviewForm),
    ('authentication', forms.CreateAllAuthenticationForm),
    ('payment', forms.CreateAllPaymentForm),
    ('address', forms.CreateAllAddressForm),
    ('comment', forms.CreateAllCommentForm),
    ('resume', forms.CreateAllResumeForm),
    # ('validation', forms.CreateAllValidationForm),
]

def show_create_all_products_form_condition(wizard):
    cart_data = wizard.get_cleaned_data_for_step('cart') or {}
    subscription_data = wizard.get_cleaned_data_for_step('subscription') or {}
    return cart_data.get('choice', 'perso') == 'perso' or subscription_data.get('customized', False)

def show_create_all_suppliers_form_condition(wizard):
    cart_data = wizard.get_cleaned_data_for_step('cart') or {}
    subscription_data = wizard.get_cleaned_data_for_step('subscription') or {}
    if cart_data.get('choice', 'perso') != 'perso' and not subscription_data.get('customized', False): return False

    products_data = wizard.get_cleaned_data_for_step('products') or {}
    extents_data = wizard.get_cleaned_data_for_step('extents') or {}

    for product in products_data.get('products', []):
        if extents_data.get('choice_supplier_product_%d' % product.id, 'false') == 'true': return True

    return False

def show_create_all_authentication_form_condition(wizard):
    # return not wizard.request.user.is_authenticated() and not wizard.storage.extra_data.get('user', None)
    return not wizard.request.user.is_authenticated()

CREATEALL_CONDITIONS = {
    'products': show_create_all_products_form_condition,
    'extents': show_create_all_products_form_condition,
    'suppliers': show_create_all_suppliers_form_condition,
    'authentication': show_create_all_authentication_form_condition,
}

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

        form.step_idx = CREATEALL_STEPS_ORDER.index(step)
        count = len(CREATEALL_STEPS_ORDER)

        form.progress_value = 0
        form.current_progress_value = 0
        if step == 'cart':
            form.progress_value = 0
        elif step == 'validation':
            form.progress_value = 100
        else:
            form.progress_value = int(form.step_idx/count*100)
            form.current_progress_value = int(1/count*100)
        form.inverse_progress_value = 100-(form.progress_value + form.current_progress_value)

        return CREATEALL_STEPS.get(step, CreateAllStep())(self, form, step, data, files)

    def process_step(self, form):
        step = self.steps.current
        print(self.storage.extra_data)
        print(self.get_all_cleaned_data())
        return super().process_step(CREATEALL_PROCESS_STEPS.get(step, CreateAllProcessStep())(self, form))

    def done(self, form_list, **kwargs):
        CREATEALL_FORMS_MIRROR = dict([(v,k) for k,v in dict(CREATEALL_FORMS).items()])
        form_data = dict([(CREATEALL_FORMS_MIRROR[f.__class__], f.cleaned_data) for f in form_list])
        print(form_data)

        tmp_dict = {}
        for f in form_list:
            step = CREATEALL_FORMS_MIRROR[f.__class__]
            print('process %s to do' % step)
            if not CREATEALL_DONE.get(step, CreateAllDone())(self, form_data[step], form_data, tmp_dict):
                break

        raise ValueError('done')
        # return HttpResponseRedirect('/carts/create/all')

    # @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs): return super().dispatch(*args, **kwargs)
