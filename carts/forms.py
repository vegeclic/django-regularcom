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
from . import models
import common.forms as cf
import common.models as cm
import products.models as pm
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
        fields = ('enabled', 'customer', 'size', 'frequency', 'duration', 'start', 'criterias', 'quantity',)

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
        fields = ('enabled', 'customer', 'size', 'criterias', 'quantity',)

class ExtentAdminForm(forms.ModelForm):
    class Meta:
        model = models.Extent

class ThematicExtentAdminForm(forms.ModelForm):
    class Meta:
        model = models.ThematicExtent

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

class CreateForm(forms.ModelForm):
    class Meta:
        model = models.Subscription
        fields = ('size', 'frequency', 'duration', 'start', 'criterias', 'quantity',)

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

class MyCheckboxSelectMultiple(forms.SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = ['<div class="btn-group" data-toggle="buttons">']
        # Normalize to strings
        str_values = set([forms.widgets.force_text(v) for v in value])
        for i, (option_value, option_label) in enumerate(forms.widgets.chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = forms.widgets.format_html(' for="{0}"', final_attrs['id'])
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = forms.widgets.force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = forms.widgets.force_text(option_label)
            output.append(forms.widgets.format_html('<label class="btn btn-default btn-lg"{0}>{1} {2}</label>',
                                                    label_for, rendered_cb, option_label))
        output.append('</div>')
        return forms.widgets.mark_safe('\n'.join(output))

    def id_for_label(self, id_):
        # See the comment for RadioSelect.id_for_label()
        if id_:
            id_ += '_0'
        return id_

class CreateForm1(forms.Form):
    size = forms.ModelChoiceField(queryset=models.Size.objects.all(), initial=models.Size.objects.all()[1],
                                  help_text=_('Which size would you like to use for your cart ?'))
    frequency = forms.ChoiceField(choices=models.FREQUENCY_CHOICES, initial=models.FREQUENCY_DEFAULT,
                                  help_text=_('How often would you like to receive your cart ?'))
    duration = forms.ChoiceField(choices=DURATION_CHOICES, initial=DURATION_DEFAULT,
                                 help_text=_('How long would you like to receive your cart ?'))
    start = forms.ChoiceField(help_text=_('When would you like to start your subscription ?'))
    customized = forms.BooleanField(required=False)
    criterias = forms.ModelMultipleChoiceField(widget=MyCheckboxSelectMultiple, queryset=cm.Criteria.objects.all(), required=False, help_text=_('Select as much criterias as you want in your cart.'))
    # products = forms.MultipleChoiceField(help_text=_('Use CTRL to select several products.'))
    # criterias = forms.MultipleChoiceField(help_text=_('Use CTRL to select several criterias.'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['products'].choices = [(product.id, product) for product in pm.Product.objects.all()]
        # self.fields['criterias'].choices = [(criteria.id, criteria) for criteria in cm.Criteria.objects.all()]

        cw = Week.withdate(Week.thisweek().sunday() + relativedelta(days=9))
        start = self.fields['start']
        start_choices = [str(w + cw.week - 1) for w in Week.weeks_of_year(cw.year)]
        start.choices = zip(start_choices, start_choices)
        start.initial = cw

        for field in ['size', 'frequency', 'duration', 'start']:
            self.fields[field].widget.attrs['class'] = 'slidebar-select'

        for field in ['criterias']:
            self.fields[field].widget.attrs['class'] = 'checkbox-select'

class CreateForm2(forms.Form):
    # extents = forms.MultipleHiddenInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class SubscriptionUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Subscription
        fields = ('direct_debit', 'enabled',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
