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
from django import forms
from django.utils.translation import ugettext_lazy as _
from itertools import chain
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.forms.util import flatatt
import django.contrib.auth as auth
from . import models
import common.forms as cf
import common.models as cm
import suppliers.models as sm
import products.models as pm
import accounts.models as am
import wallets.models as wm
import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week
from pprint import pprint

DURATION_CHOICES = (
    (1, _('1 month')),
    (3, _('3 months')),
    (6, _('6 months')),
    (9, _('9 months')),
    (12, _('1 year')),
    (18, _('18 months')),
    (24, _('2 years')),
)

DURATION_DEFAULT = 3

class PriceAdminForm(cf.ModelFormWithCurrency):
    class Meta:
        model = models.Price

class SubscriptionBaseAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        prefix = 'extent_set-'
        total = int(self.data.get('%sTOTAL_FORMS' % prefix))
        extents = [int(e) if e else 0 for e in [self.data.get('%s%d-extent' % (prefix,i)) for i in range(total)]]
        count = sum([e > 0 for e in extents])
        count_delete = sum([self.data.get('%s%d-DELETE' % (prefix,i), 'off') == 'on' for i in range(total)])
        count -= count_delete
        __sum = sum(extents)
        if count and __sum != 100:
            raise forms.ValidationError(_('The sum of extents should be equal to 100 instead %d.' % __sum))
        return cleaned_data

class SubscriptionCreationAdminForm(SubscriptionBaseAdminForm):
    class Meta:
        model = models.Subscription
        fields = ('enabled', 'customer', 'size', 'carrier', 'receive_only_once', 'frequency', 'duration', 'start', 'criterias', 'quantity', 'comment',)

    duration = forms.ChoiceField(choices=DURATION_CHOICES, initial=3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        start = self.fields['start']
        cw = Week.thisweek()
        choices = [str(w + cw.week) for w in Week.weeks_of_year(cw.year)]
        start.choices = zip(choices, choices)
        start.initial = cw+1

    def save(self, commit=True):
        subscription = super().save(commit=False)
        bw = Week.fromstring(self.cleaned_data['start'])
        ew = Week.withdate( bw.day(1) + relativedelta(months=int(self.cleaned_data['duration'])) )
        subscription.end = ew
        if commit:
            subscription.save()
            subscription.create_deliveries()
        return subscription

class SubscriptionAdminForm(SubscriptionBaseAdminForm):
    class Meta:
        model = models.Subscription
        fields = ('enabled', 'customer', 'size', 'carrier', 'criterias', 'quantity', 'comment',)

class ExtentAdminForm(forms.ModelForm):
    class Meta:
        model = models.Extent

class ThematicExtentAdminForm(forms.ModelForm):
    class Meta:
        model = models.ThematicExtent

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = pm.Product.objects.order_by('name')

class DeliveryCreationAdminForm(forms.ModelForm):
    class Meta:
        model = models.Delivery

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        date = self.fields['date']
        cw = Week.thisweek()
        choices = [str(w + cw.week) for w in Week.weeks_of_year(cw.year)]
        date.choices = zip(choices, choices)
        date.initial = cw+1

class DeliveryAdminForm(forms.ModelForm):
    class Meta:
        model = models.Delivery

class ContentAdminForm(forms.ModelForm):
    class Meta:
        model = models.Content

class ExtentContentAdminForm(forms.ModelForm):
    class Meta:
        model = models.ExtentContent

class MyCheckboxSelectMultiple(forms.SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = ['<div class="btn-group" data-toggle="buttons">']
        # Normalize to strings
        str_values = set([force_text(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = format_html(' for="{0}"', final_attrs['id'])
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = force_text(option_label)
            output.append(format_html('<label class="btn btn-default btn-lg {0} {1}"{2}>{3} {4}</label>',
                                                    'active' if cb.check_test(option_value) else '',
                                                    'disabled' if 'disabled' in attrs else '',
                                                    label_for, rendered_cb, option_label))
        output.append('</div>')
        return mark_safe('\n'.join(output))

    def id_for_label(self, id_):
        # See the comment for RadioSelect.id_for_label()
        if id_:
            id_ += '_0'
        return id_

class MyRadioInput(forms.widgets.SubWidget):
    """
    An object used by RadioFieldRenderer that represents a single
    <input type='radio'>.
    """

    def __init__(self, name, value, attrs, choice, index):
        self.name, self.value = name, value
        self.attrs = attrs
        self.choice_value = force_text(choice[0])
        self.choice_label = force_text(choice[1])
        self.index = index

    def __str__(self):
        return self.render()

    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        if 'id' in self.attrs:
            label_for = format_html(' for="{0}_{1}"', self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = force_text(self.choice_label)
        return format_html('<label class="btn btn-default btn-lg {0} {1}" {2}>{3} {4}</label>',
                           'active' if self.is_checked() else '',
                           'disabled' if 'disabled' in attrs else '',
                           label_for, self.tag(), choice_label)

    def is_checked(self):
        return int(self.value) == int(self.choice_value)

    def tag(self):
        if 'id' in self.attrs:
            self.attrs['id'] = '%s_%s' % (self.attrs['id'], self.index)
        final_attrs = dict(self.attrs, type='radio', name=self.name, value=self.choice_value)
        if self.is_checked():
            final_attrs['checked'] = 'checked'
        return format_html('<input{0} />', flatatt(final_attrs))

class MyRadioFieldRenderer(object):
    """
    An object used by RadioSelect to enable customization of radio widgets.
    """

    def __init__(self, name, value, attrs, choices):
        self.name, self.value, self.attrs = name, value, attrs
        self.choices = choices

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield MyRadioInput(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx] # Let the IndexError propogate
        return MyRadioInput(self.name, self.value, self.attrs.copy(), choice, idx)

    def __str__(self):
        return self.render()

    def render(self):
        """Outputs a <div> for this set of radio fields."""
        return format_html('<div class="btn-group" data-toggle="buttons">\n{0}\n</div>', format_html_join('\n', '{0}', [(force_text(w),) for w in self]))

class CreateForm1(forms.Form):
    size = forms.ModelChoiceField(queryset=models.Size.objects.select_related().order_by('weight'), initial=2,
                                  help_text=_('Which size would you like to use for your cart ? (delivery fees included)'),
                                  label=_('Size'))
    frequency = forms.ChoiceField(choices=models.FREQUENCY_CHOICES, initial=models.FREQUENCY_DEFAULT,
                                  help_text=_('How often would you like to receive your cart ?'),
                                  label=_('Frequency'))
    duration = forms.ChoiceField(choices=DURATION_CHOICES, initial=DURATION_DEFAULT,
                                 help_text=_('How long would you like to receive your cart ?'),
                                 label=_('Duration'))
    start = forms.ChoiceField(help_text=_('When would you like to start your subscription ?'),
                              label=_('Beginning of your subscription'))
    criterias = forms.ModelMultipleChoiceField(widget=MyCheckboxSelectMultiple,
                                               queryset=cm.Criteria.objects.select_related().filter(enabled=True).order_by('id'),
                                               required=False, label=_('Criterias'),
                                               help_text=_('Select as much criterias as you want in your cart.'))
    carrier = forms.ModelChoiceField(widget=forms.RadioSelect(renderer=MyRadioFieldRenderer),
                                     queryset=models.Carrier.objects.select_related().order_by('id'), initial=3,
                                     help_text=_('Which carrier would you like to use for your cart ? (delivery fees included)'),
                                     label=_('Carrier'))

    customized = forms.BooleanField(label=_('Customized'), required=False)
    receive_only_once = forms.BooleanField(label=_('Receive only once'), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cw = Week.withdate(Week.thisweek().sunday() + relativedelta(days=9))
        start = self.fields['start']
        start_choices = [str(w + cw.week - 1) for w in Week.weeks_of_year(cw.year)]
        start_date_choices = ['%s (%s %s)' % ((w + cw.week - 1).day(settings.DELIVERY_DAY_OF_WEEK).strftime('%d-%m-%Y'), _('Week'), (w + cw.week - 1).week) for w in Week.weeks_of_year(cw.year)]
        start.choices = zip(start_choices, start_date_choices)
        start.initial = cw

        for field in ['size', 'frequency', 'duration', 'start']:
            self.fields[field].widget.attrs['class'] = 'slidebar-select'

        for field in ['criterias', 'receive_only_once']:
            self.fields[field].widget.attrs['class'] = 'checkbox-select'

        for field in ['carrier']:
            self.fields[field].widget.attrs['class'] = 'radio-select'

class CreateForm2(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class SubscriptionUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Subscription
        fields = ('direct_debit', 'enabled',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CreateAllCartForm(forms.Form):
    choice = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CreateAllSubscriptionForm(forms.Form):
    size = forms.ModelChoiceField(queryset=models.Size.objects.select_related().order_by('weight'), initial=2,
                                  help_text=_('Which size would you like to use for your cart ? (delivery fees included)'),
                                  label=_('Size'))
    frequency = forms.ChoiceField(choices=models.FREQUENCY_CHOICES, initial=models.FREQUENCY_DEFAULT,
                                  help_text=_('How often would you like to receive your cart ?'),
                                  label=_('Frequency'))
    duration = forms.ChoiceField(choices=DURATION_CHOICES, initial=DURATION_DEFAULT,
                                 help_text=_('How long would you like to receive your cart ?'),
                                 label=_('Duration'))
    start = forms.ChoiceField(help_text=_('When would you like to start your subscription ?'),
                              label=_('Beginning of your subscription'))
    criterias = forms.ModelMultipleChoiceField(widget=MyCheckboxSelectMultiple,
                                               queryset=cm.Criteria.objects.select_related().filter(enabled=True).order_by('id'),
                                               required=False, label=_('Criterias'),
                                               help_text=_('Select as much criterias as you want in your cart.'))
    carrier = forms.ModelChoiceField(widget=forms.RadioSelect(renderer=MyRadioFieldRenderer),
                                     queryset=models.Carrier.objects.select_related().order_by('id'), initial=3,
                                     help_text=_('Which carrier would you like to use for your cart ? (delivery fees included)'),
                                     label=_('Carrier'))

    customized = forms.BooleanField(label=_('Customized'), required=False, initial=True)
    receive_only_once = forms.BooleanField(label=_('Receive only once'), required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cw = Week.withdate(Week.thisweek().sunday() + relativedelta(days=9))
        start = self.fields['start']
        start_choices = [str(w + cw.week - 1) for w in Week.weeks_of_year(cw.year)]
        start_date_choices = ['%s (%s %s)' % ((w + cw.week - 1).day(settings.DELIVERY_DAY_OF_WEEK).strftime('%d-%m-%Y'), _('Week'), (w + cw.week - 1).week) for w in Week.weeks_of_year(cw.year)]
        start.choices = zip(start_choices, start_date_choices)
        start.initial = cw

        for field in ['size', 'frequency', 'duration', 'start']:
            self.fields[field].widget.attrs['class'] = 'slidebar-select'

        for field in ['criterias', 'receive_only_once']:
            self.fields[field].widget.attrs['class'] = 'checkbox-select'

        for field in ['carrier']:
            self.fields[field].widget.attrs['class'] = 'radio-select'

class CreateAllProductsForm(forms.Form):
    products = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                              queryset=pm.Product.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CreateAllExtentsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MyImageCheckboxSelectMultiple(forms.SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = ['<div class="btn-group" data-toggle="buttons">']
        # Normalize to strings
        str_values = set([force_text(v) for v in value])
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = format_html(' for="{0}"', final_attrs['id'])
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = force_text(option_label)
            option_labels = option_label.split('|#~|')
            output.append(format_html('<label class="choice btn btn-default btn-lg {0} {1}"{2}>{3} <img class="img-thumbnail tooltip_link" src="{4}{5}" style="width:100px" title="{6}" alt="{6}"/><span class="price">{7}</span></label>',
                                                    'active' if cb.check_test(option_value) else '',
                                                    'disabled' if 'disabled' in attrs else '',
                                                    label_for, rendered_cb, settings.MEDIA_URL, option_labels[1], option_labels[0], option_labels[2]))
        output.append('</div>')
        return mark_safe('\n'.join(output))

    def id_for_label(self, id_):
        # See the comment for RadioSelect.id_for_label()
        if id_:
            id_ += '_0'
        return id_

class CreateAllSuppliersForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CreateAllPreviewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CreateAllAuthenticationForm(forms.Form):
    sign_type = forms.ChoiceField(widget=forms.RadioSelect(renderer=MyRadioFieldRenderer), label='Type', initial = 'up', choices = [('up', _('Inscription')), ('in', _('Connexion'))], required=False)
    email = forms.EmailField(label=_('Email address'), max_length=255, required=False)
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'), required=False)

    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'incorrect': _("Vos identifiants de connexion sont incorrects. Si vous n'êtes pas encore inscrit, nous vous invitons à vous inscrire en cliquant sur « Inscription » dans le cas contraire, cliquez sur le lien « J'ai oublié mon mot de passe »."),
        'empty': _('Users must have an email address'),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ['sign_type', 'email', 'password']:
            f = self.fields.get(field)
            attrs = f.widget.attrs
            attrs['class'] = 'form-control'

        for field in ['email', 'password']:
            f = self.fields.get(field)
            attrs = f.widget.attrs
            attrs['placeholder'] = f.label

    def clean(self):
        print(self.user)

        if self.user: return super().clean()

        email = self.cleaned_data['email'].lower()

        if not email:
            raise forms.ValidationError(self.error_messages['empty'])

        if self.cleaned_data['sign_type'] == 'up':
            try:
                am.Account._default_manager.get(email=email)
            except am.Account.DoesNotExist:
                return super().clean()
            raise forms.ValidationError(self.error_messages['duplicate_email'])

        # sign in
        password = self.cleaned_data['password']
        user = auth.authenticate(username=email, password=password)
        if user is None:
            raise forms.ValidationError(self.error_messages['incorrect'])
        return super().clean()

class CreateAllPaymentForm(forms.Form):
    nb_deliveries = forms.ChoiceField(help_text=_("Choisissez le nombre d'échéance que vous souhaitez payer."), label=_("Nombre d'échéances à payer"))
    payment_type = forms.ChoiceField(widget=forms.RadioSelect(renderer=MyRadioFieldRenderer), label=_('payment type'), choices=wm.PAYMENT_TYPES, initial='c', help_text=_('Choisissez votre type de paiement.'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('payment_type').widget.attrs['class'] = 'radio-select'

        for field in ['nb_deliveries']:
            self.fields[field].widget.attrs['class'] = 'slidebar-select'

class CreateAllAddressForm(forms.Form):
    gender = forms.ChoiceField(widget=forms.RadioSelect(renderer=MyRadioFieldRenderer), label=_('Gender'), choices=cm.Address.GENDER_CHOICES, required=False)
    first_name = forms.CharField(label=_('First name'), max_length=30, required=False)
    last_name = forms.CharField(label=_('Last name'), max_length=30, required=False)
    street = forms.CharField(widget=forms.Textarea, label=_('Street'), max_length=100, required=False)
    postal_code = forms.CharField(label=_('Postal code'), max_length=100, required=False)
    city = forms.CharField(label=_('City'), max_length=100, required=False)
    country = forms.ModelChoiceField(widget=forms.RadioSelect(renderer=MyRadioFieldRenderer), queryset=cm.Country.objects.all(), label=_('Country'), required=False, empty_label=None)
    home_phone = forms.CharField(label=_('Home phone'), max_length=100, required=False)
    mobile_phone = forms.CharField(label=_('Mobile phone'), max_length=100, required=False)

    relay_name = forms.CharField(label=_('Relay name'), max_length=100, required=False)
    relay_street = forms.CharField(widget=forms.Textarea, label=_('Relay street'), max_length=100, required=False)
    relay_postal_code = forms.CharField(label=_('Relay postal code'), max_length=100, required=False)
    relay_city = forms.CharField(label=_('Relay city'), max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            f = self.fields.get(field)
            attrs = f.widget.attrs
            attrs['class'] = 'form-control'

        for field in ['first_name', 'last_name', 'street', 'postal_code', 'city', 'home_phone', 'mobile_phone', 'relay_name', 'relay_street', 'relay_postal_code', 'relay_city']:
            f = self.fields.get(field)
            attrs = f.widget.attrs
            attrs['placeholder'] = f.label

        for field in ['street', 'relay_street']:
            self.fields.get(field).widget.attrs['rows'] = 3

class CreateAllCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, label=_('Write down your comment here.'), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            f = self.fields.get(field)
            attrs = f.widget.attrs
            attrs['class'] = 'form-control'

        for field in ['comment']:
            f = self.fields.get(field)
            attrs = f.widget.attrs
            attrs['placeholder'] = f.label

class CreateAllResumeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
