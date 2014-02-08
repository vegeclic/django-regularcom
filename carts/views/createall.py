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
from django.contrib.contenttypes.models import ContentType
import django.contrib.auth as auth
import common.models as cm
import customers.models as csm
import products.models as pm
import suppliers.models as sm
import mailbox.models as mm
import suppliers.views as sw
import accounts.models as am
import wallets.models as wm
from .. import forms, models
import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week
import numpy as np

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
        user_id = wizard.storage.extra_data.get('user_id', None)
        user = am.Account.objects.get(id=user_id) if user_id else None
    return user

def get_thematic(cart_data):
    thematic = None
    try:
        choice = int(cart_data.get('choice', None))
        __key = 'thematic_%d' % choice
        thematic = cache.get(__key) or models.Thematic.objects.select_related().get(id=choice)
        if not cache.get(__key): cache.set(__key, thematic)
    except models.Thematic.DoesNotExist:
        thematic = None
    except ValueError:
        thematic = None
    except TypeError:
        thematic = None
    return thematic

class CreateAllCartStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        form.thematic_list = cache.get('thematic_list') or models.Thematic.objects.filter(enabled=True).select_related('main_image').order_by('name').all()
        if not cache.get('thematic_list'): cache.set('thematic_list', form.thematic_list)
        return form

class CreateAllSubscriptionStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        cart_data = wizard.get_cleaned_data_for_step('cart') or {}

        form.thematic = get_thematic(cart_data)

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

            if form.thematic.criterias:
                __key = 'thematic_criterias_%d' % form.thematic.id
                form.fields['criterias'].initial = cache.get(__key) or [v.id for v in form.thematic.criterias.all()]
                if not cache.get(__key): cache.set(__key, form.fields['criterias'].initial)

            form.fields['receive_only_once'].initial = form.thematic.receive_only_once
            form.fields['customized'].initial = False

            for field, locked in [('size', form.thematic.locked_size),
                                  ('carrier', form.thematic.locked_carrier),
                                  ('receive_only_once', form.thematic.locked_receive_only_once),
                                  ('frequency', form.thematic.locked_frequency),
                                  ('start', form.thematic.locked_start),
                                  ('duration', form.thematic.locked_duration),
                                  ('criterias', form.thematic.locked_criterias),
                                  ('customized', form.thematic.locked_products)]:
                if locked:
                    attrs = form.fields[field].widget.attrs
                    attrs['class'] = attrs.get('class', '') + ' disabled'
        else:
            form.fields['customized'].initial = True
            attrs = form.fields['customized'].widget.attrs
            attrs['class'] = attrs.get('class', '') + ' disabled'

        form.carriers = cache.get('create_carriers') or models.Carrier.objects.select_related().all()
        if not cache.get('create_carriers'): cache.set('create_carriers', form.carriers)

        form.sizes = cache.get('create_sizes') or models.Size.objects.select_related().order_by('order').all()
        if not cache.get('create_sizes'): cache.set('create_sizes', form.sizes)

        return form

class CreateAllSubscriptionDone(CreateAllDone):
    def __call__(self, wizard, own_data, form_data, tmp_dict):
        # print('subscription done')

        # print(tmp_dict)

        user = get_user(wizard)
        customer = user.customer
        thematic = get_thematic(form_data['cart'])
        customized = own_data.get('customized', False)

        duration = int(own_data.get('duration'))
        bw = Week.fromstring(own_data.get('start'))
        ew = Week.withdate( bw.day(1) + relativedelta(months=duration) )

        subscription = models.Subscription.objects.create(customer=customer, size=own_data['size'], carrier=own_data['carrier'], receive_only_once=own_data['receive_only_once'], frequency=int(own_data['frequency']), start=bw, end=ew, comment=form_data['comment'].get('comment', ''))

        subscription.criterias = own_data['criterias']

        if thematic and not customized:
            for e in thematic.thematicextent_set.all():
                subscription.extent_set.create(product=e.product, extent=e.extent, customized=False)

        subscription.create_deliveries()

        tmp_dict['subscription'] = subscription

        deliveries = subscription.delivery_set.order_by('date')

        mm.Message.objects.create_message(participants=[customer], subject=_('Votre abonnement %(subscription_id)d a été crée') % {'subscription_id': subscription.id}, body=_(
"""Bonjour %(name)s,

Nous sommes heureux de vous annoncer que votre abonnement %(subscription_id)d a été crée, il est accessible à l'adresse suivante :

http://www.vegeclic.fr/carts/subscriptions/%(subscription_id)d/deliveries/

Bien cordialement,
Végéclic.
"""
        ) % {'name': customer.main_address.__unicode__() if customer.main_address else '', 'date': deliveries[0].get_date_display(), 'subscription_id': subscription.id})

        return True

class CreateAllProductsStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        cart_data = wizard.get_cleaned_data_for_step('cart') or {}
        form.thematic = get_thematic(cart_data)
        if form.thematic:
            __key = 'thematic_extents_%d' % form.thematic.id
            thematic_extents = cache.get(__key) or form.thematic.thematicextent_set.select_related('product').all() if form.thematic else []
            if not cache.get(__key): cache.set(__key, thematic_extents)

            form.thematic_products = [e.product for e in thematic_extents]

        form.modified = True if data else False

        form.products_tree = cache.get('products_tree') or sw.get_products_tree(pm.Product.objects)
        if not cache.get('products_tree'): cache.set('products_tree', form.products_tree)

        return form

class CreateAllProductsDone(CreateAllDone):
    def __call__(self, wizard, own_data, form_data, tmp_dict):
        subscription = tmp_dict['subscription']

        # print('products', subscription)

        products_data = form_data.get('products') or {}
        extents_data = form_data.get('extents') or {}
        suppliers_data = form_data.get('suppliers') or {}

        products = products_data.get('products', [])

        for product in products:
            extent_value = extents_data.get('product_%d' % product.id, 0)
            custom = extents_data.get('choice_supplier_product_%d' % product.id, 'false') == 'true'
            extent = subscription.extent_set.create(product=product, extent=extent_value, customized=custom)

            if custom:
                supplier_products = suppliers_data.get('supplier_product_%d' % product.id) or []
                extent_content = extent.extentcontent_set.create()
                for sp in supplier_products:
                    extent_content.extentcontentproduct_set.create(product=sp, quantity=1)

        return True

SUPPLIER_PRODUCTS_CHOICES = [
    ('false', _('Je laisse Végéclic choisir')),
    ('true', _('Je souhaite choisir')),
]

class CreateAllExtentsStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        products_data = wizard.get_cleaned_data_for_step('products') or {}
        cart_data = wizard.get_cleaned_data_for_step('cart') or {}
        form.thematic = get_thematic(cart_data)

        products = products_data.get('products', [])

        thematic_extents = []
        if form.thematic:
            __key = 'thematic_extents_%d' % form.thematic.id
            thematic_extents = cache.get(__key) or form.thematic.thematicextent_set.select_related('product').all() if form.thematic else []
            if not cache.get(__key): cache.set(__key, thematic_extents)

        thematic_products = [e.product for e in thematic_extents] if form.thematic else []
        extents = [e.extent for e in thematic_extents] if form.thematic else []
        shared_extent = int((100 - sum(extents))/(len(products) - len(extents))) if (len(products) - len(extents)) else 0

        for product in products:
            extent = form.thematic.thematicextent_set.get(product=product) if product in thematic_products else None
            form.fields['product_%d' % product.id] = f1 = forms.forms.IntegerField(widget=forms.forms.HiddenInput, label=product.name, initial=extent.extent if extent else shared_extent, min_value=0, max_value=100)
            form.fields['choice_supplier_product_%d' % product.id] = f2 = forms.forms.ChoiceField(widget=forms.forms.RadioSelect(renderer=forms.MyRadioFieldRenderer), label='boolean')
            f2.choices = SUPPLIER_PRODUCTS_CHOICES
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
        carrier = subscription_data.get('carrier', None)

        products_tree = cache.get('products_tree') or sw.get_products_tree(pm.Product.objects)
        if not cache.get('products_tree'): cache.set('products_tree', products_tree)

        for product in products:
            if extents_data.get('choice_supplier_product_%d' % product.id, 'false') == 'false': continue
            weight = size.weight - size.weight*settings.PACKAGING_WEIGHT_RATE/100
            price = size.default_price().price
            weight_level = carrier.carrierlevel_set.filter(weight__gte=size.weight)
            if weight_level: price -= weight_level[0].price
            price = price*extents_data.get('product_%d' % product.id, 1)/100

            root = sw.find_product(products_tree, product.id)
            qs = sm.Product.objects.filter(status='p', product__in=sw.products_tree_to_list(root)).select_related('main_image', 'main_price', 'main_price__currency', 'main_price__tax', 'main_price__supplier').prefetch_related('criterias', 'suppliers').order_by('-date_created')
            form.fields['supplier_product_%d' % product.id] = f = forms.forms.ModelMultipleChoiceField(widget=forms.createall.MyImageCheckboxSelectMultiple, queryset=qs, label=product.name)
            supplier_products_list = qs.all()
            f.choices = [(p.id, '%s|#~|%s|#~|%s' % (p.name, p.main_image.image if p.main_image else '', (p.main_price.get_after_tax_price_with_fee() if carrier.apply_suppliers_fee else p.main_price.get_after_tax_price())/price*100)) for p in supplier_products_list]

        return form

def get_deliveries(nb, init_price):
    price_rate = 1+settings.DEGRESSIVE_PRICE_RATE/100
    return np.array([init_price/price_rate**k for k in range(nb)])

def get_deliveries_from_subscription(subscription_data):
    receive_only_once = subscription_data.get('receive_only_once')
    bw = Week.fromstring(str(subscription_data.get('start')))
    ew = Week.withdate( bw.day(1) + relativedelta(months=int(subscription_data.get('duration'))) )
    nb = len(range(0, ew+1-bw, int(subscription_data.get('frequency'))))
    init_price = subscription_data.get('size').default_price().price
    prices = get_deliveries(nb, init_price)
    if receive_only_once: prices = np.array([prices[0]])
    deliveries = [(i+1, '%s (%s %s)' % ((bw+i*2).day(settings.DELIVERY_DAY_OF_WEEK).strftime('%d-%m-%Y'), _('Week'), (bw+i*2).week), p) for i,p in enumerate(prices)]
    return deliveries, prices

class CreateAllPreviewStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        subscription_data = wizard.get_cleaned_data_for_step('subscription') or {}
        if not subscription_data: return form

        cart_data = wizard.get_cleaned_data_for_step('cart') or {}
        if not cart_data: return form

        form.thematic = get_thematic(cart_data)
        form.size = subscription_data.get('size')
        form.duration = dict(forms.DURATION_CHOICES).get(int(subscription_data.get('duration')))
        w = Week.fromstring(subscription_data.get('start'))
        form.start = '%s (%s %s)' % (w.day(settings.DELIVERY_DAY_OF_WEEK).strftime('%d-%m-%Y'), _('Week'), w.week)
        form.frequency = dict(models.FREQUENCY_CHOICES).get(int(subscription_data.get('frequency')))
        form.receive_only_once = subscription_data.get('receive_only_once')

        products_data = wizard.get_cleaned_data_for_step('products') or {}
        extents_data = wizard.get_cleaned_data_for_step('extents') or {}
        suppliers_data = wizard.get_cleaned_data_for_step('suppliers') or {}

        products = products_data.get('products') or []

        form.products = []

        if products:
            for product in products:
                form.products.append((product,
                                      extents_data.get('product_%d' % product.id),
                                      extents_data.get('choice_supplier_product_%d' % product.id, 'false'),
                                      suppliers_data.get('supplier_product_%d' % product.id)))
        else:
            if form.thematic:
                __key = 'thematic_extents_%d' % form.thematic.id
                thematic_extents = cache.get(__key) or form.thematic.thematicextent_set.select_related('product').all() if form.thematic else []
                if not cache.get(__key): cache.set(__key, thematic_extents)

                for e in thematic_extents:
                    form.products.append((e.product, e.extent, 'false', []))

        form.supplier_products_choices = SUPPLIER_PRODUCTS_CHOICES

        form.deliveries, prices = get_deliveries_from_subscription(subscription_data)
        form.sum_of_prices, form.mean_of_prices = prices.sum(), prices.mean()

        return form

class CreateAllAuthenticationStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        form.user = get_user(wizard)
        return form

class CreateAllAuthenticationProcessStep(CreateAllProcessStep):
    def __call__(self, wizard, form):
        if not form.cleaned_data: return form
        if get_user(wizard): return form

        email = form.cleaned_data.get('email').lower()

        if form.cleaned_data.get('sign_type') == 'up':
            user = am.Account.objects.create_user(email=email)
            backend = auth.get_backends()[0]
            user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
            wizard.storage.extra_data['user_id'] = user.id
            wizard.storage.extra_data['user_backend'] = user.backend
            messages.success(wizard.request, _("Your account has been successfully created."))

            # print('authentication sign up')

            return form

        # sign in
        password = form.cleaned_data.get('password')
        user = auth.authenticate(username=email, password=password)
        if user is None: raise forms.forms.ValidationError(_('bad credentials'))
        wizard.storage.extra_data['user_id'] = user.id
        wizard.storage.extra_data['user_backend'] = user.backend
        messages.success(wizard.request, _("You're logged in."))

        # print('authentication sign in')

        return form

class CreateAllPaymentStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        subscription_data = wizard.get_cleaned_data_for_step('subscription') or {}
        if not subscription_data: return form

        user = get_user(wizard)
        if user:
            form.balance = user.customer.wallet.balance_in_target_currency()
            form.balance_inversed = form.balance*-1
            form.currency = user.customer.wallet.target_currency

        form.receive_only_once = subscription_data.get('receive_only_once')
        form.price = subscription_data.get('size').default_price()
        form.price_rate = 1+settings.DEGRESSIVE_PRICE_RATE/100

        bw = Week.fromstring(str(subscription_data.get('start')))
        ew = Week.withdate( bw.day(1) + relativedelta(months=int(subscription_data.get('duration'))) )
        deliveries, prices = get_deliveries_from_subscription(subscription_data)

        form.fields['nb_deliveries'].choices = [(k+1, '%d %s' % (k+1, _('échéance(s)'))) for k in range(len(prices))]

        return form

class CreateAllPaymentDone(CreateAllDone):
    def __call__(self, wizard, own_data, form_data, tmp_dict):
        user = get_user(wizard)
        subscription_data = form_data['subscription']
        t = own_data['payment_type']
        nb = int(own_data['nb_deliveries'])

        size_price = subscription_data.get('size').default_price()
        init_price = size_price.price
        currency = size_price.currency
        prices = get_deliveries(nb, init_price)
        amount = round(prices.sum(),2)
        balance = user.customer.wallet.balance

        subscription = tmp_dict['subscription']

        if balance < amount:
            wm.Credit.objects.create(wallet=user.customer.wallet, payment_type=t, amount=round(amount-balance,2), currency=currency)
        else:
            for i,delivery in enumerate(subscription.delivery_set.order_by('date').all()):
                if i >= nb: break
                delivery.status = 'p'
                delivery.save()

        return True

class CreateAllAddressStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        subscription_data = wizard.get_cleaned_data_for_step('subscription') or {}
        if not subscription_data: return form

        user = get_user(wizard)
        if not user: return form

        if user.customer.main_address:
            address = user.customer.main_address
            for k, f in [('first_name', address.first_name), ('last_name', address.last_name),
                         ('street', address.street), ('postal_code', address.postal_code),
                         ('city', address.city), ('country', address.country),
                         ('home_phone', address.home_phone), ('mobile_phone', address.mobile_phone)]:
                form.fields[k].initial = f

        if user.customer.relay_address:
            relay = user.customer.relay_address
            for k, f in [('relay_name', relay.last_name), ('relay_street', relay.street),
                         ('relay_postal_code', relay.postal_code), ('relay_city', relay.city)]:
                form.fields[k].initial = f

        form.is_relay = subscription_data.get('carrier').id == 3

        return form

class CreateAllAddressDone(CreateAllDone):
    def __call__(self, wizard, own_data, form_data, tmp_dict):
        user = get_user(wizard)

        user.customer.main_address = ma = user.customer.main_address or cm.Address.objects.create(content_type=ContentType.objects.get(app_label='customers', model='customer'), object_id=user.customer.id)
        ma.first_name = own_data['first_name']; ma.last_name = own_data['last_name']
        ma.street = own_data['street']; ma.postal_code = own_data['postal_code']
        ma.city = own_data['city']; ma.country = own_data['country']
        ma.home_phone = own_data['home_phone']; ma.mobile_phone = own_data['mobile_phone']
        ma.save()

        if form_data['subscription'].get('carrier').id == 3:
            user.customer.relay_address = ra = user.customer.relay_address or cm.Address.objects.create(content_type=ContentType.objects.get(app_label='customers', model='customer'), object_id=user.customer.id)
            ra.last_name = own_data['relay_name']; ra.street = own_data['relay_street']
            ra.postal_code = own_data['relay_postal_code']; ra.city = own_data['relay_city']
            ra.save()

        user.customer.save()

        return True

class CreateAllCommentStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        return form

class CreateAllResumeStep(CreateAllStep):
    def __call__(self, wizard, form, step, data, files):
        subscription_data = wizard.get_cleaned_data_for_step('subscription') or {}
        if not subscription_data: return form
        address_data = wizard.get_cleaned_data_for_step('address') or {}
        if not address_data: return form
        form.address = address_data
        form.is_relay = subscription_data.get('carrier').id == 3
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
}

CREATEALL_PROCESS_STEPS = {
    'authentication': CreateAllAuthenticationProcessStep(),
}

CREATEALL_DONE = {
    'subscription': CreateAllSubscriptionDone(),
    'products': CreateAllProductsDone(),
    'address': CreateAllAddressDone(),
    'payment': CreateAllPaymentDone(),
}

CREATEALL_STEPS_ORDER = ['cart', 'subscription', 'products', 'extents', 'suppliers', 'preview', 'authentication', 'payment', 'address', 'comment', 'resume',]

CREATEALL_FORMS = [
    ('cart', forms.createall.CreateAllCartForm),
    ('subscription', forms.createall.CreateAllSubscriptionForm),
    ('products', forms.createall.CreateAllProductsForm),
    ('extents', forms.createall.CreateAllExtentsForm),
    ('suppliers', forms.createall.CreateAllSuppliersForm),
    ('preview', forms.createall.CreateAllPreviewForm),
    ('authentication', forms.createall.CreateAllAuthenticationForm),
    ('payment', forms.createall.CreateAllPaymentForm),
    ('address', forms.createall.CreateAllAddressForm),
    ('comment', forms.createall.CreateAllCommentForm),
    ('resume', forms.createall.CreateAllResumeForm),
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
        context.update(self.kwargs)
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
        else:
            form.progress_value = int(form.step_idx/count*100)
            form.current_progress_value = int(1/count*100)
        form.inverse_progress_value = 100-(form.progress_value + form.current_progress_value)

        return CREATEALL_STEPS.get(step, CreateAllStep())(self, form, step, data, files)

    def process_step(self, form):
        step = self.steps.current
        return super().process_step(CREATEALL_PROCESS_STEPS.get(step, CreateAllProcessStep())(self, form))

    def done(self, form_list, **kwargs):
        CREATEALL_FORMS_MIRROR = dict([(v,k) for k,v in dict(CREATEALL_FORMS).items()])
        form_data = dict([(CREATEALL_FORMS_MIRROR[f.__class__], f.cleaned_data) for f in form_list])
        tmp_dict = {}
        for f in form_list:
            step = CREATEALL_FORMS_MIRROR[f.__class__]
            # print('process %s to do' % step)
            if not CREATEALL_DONE.get(step, CreateAllDone())(self, form_data[step], form_data, tmp_dict): break

        # print('done finished')

        subscription = tmp_dict['subscription']

        if not self.request.user.is_authenticated():
            user = get_user(self)
            user.backend = self.storage.extra_data['user_backend']
            auth.login(self.request, user)

        payment_data = form_data.get('payment') or {}
        success_url = reverse_lazy('create_all_validation', args=[subscription.id, payment_data.get('payment_type', 'c'), payment_data.get('nb_deliveries', 1)])
        return HttpResponseRedirect(str(success_url))

    # @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs): return super().dispatch(*args, **kwargs)

class CreateAllValidation(generic.DetailView):
    model = models.Subscription
    template_name = 'carts/create_all/validation.html'

    def get_object(self):
        subscription_id = self.kwargs.get('subscription_id')
        return self.model.objects.get(id=subscription_id, customer__account=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'cart'
        context['sub_section'] = 'create_all'
        context['validation'] = True
        context['wizard'] = {'form': {'step_idx': 11,
                                      'progress_value': 100,
                                      'current_progress_value': 0,
                                      'inverse_progress_value': 0},
                             'steps': {'current': 'validation'}}
        context['payment_types'] = wm.PAYMENT_TYPES
        context['payment_type'] = self.kwargs.get('payment_type', 'c')
        context['nb_deliveries'] = nb = int(self.kwargs.get('nb_deliveries', '1'))
        context['wallet'] = w = self.request.user.customer.wallet
        context['balance'] = balance = w.balance
        context['balance_inversed'] = w.balance*-1
        context['target_symbol'] = w.target_currency.symbol
        context['payed_deliveries'] = self.get_object().delivery_set.filter(status='p').exists()
        context['price'] = price = self.get_object().size.default_price()
        prices = get_deliveries(nb, price.price)
        __sum = prices.sum()
        context['total_amount'] = amount = round(__sum-balance, 2)
        if amount < 0: context['total_amount'] = amount = 0
        context['mean'] = mean = round(prices.mean(), 2)

        context['cheque_nb'] = cheque_nb = int(amount/mean)
        context['cheque_first_amount'] = round(amount-cheque_nb*mean, 2)

        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs): return super().dispatch(*args, **kwargs)
