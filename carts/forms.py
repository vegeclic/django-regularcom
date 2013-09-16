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

class ThematicAdminForm(cf.ModelFormWithImage):
    class Meta:
        model = models.Thematic

class ThematicCreationAdminForm(forms.ModelForm):
    class Meta:
        model = models.Thematic
        exclude = ('main_image',)

class SizeAdminForm(cf.ModelFormWithImage):
    class Meta:
        model = models.Size

class SizeCreationAdminForm(forms.ModelForm):
    class Meta:
        model = models.Size
        exclude = ('main_image',)

class PriceAdminForm(cf.ModelFormWithCurrency):
    class Meta:
        model = models.Price

class SubscriptionBaseAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(SubscriptionBaseAdminForm, self).clean()
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
        fields = ('status', 'customer', 'size', 'frequency', 'duration', 'start', 'criterias', 'quantity',)

    duration = forms.ChoiceField(choices=DURATION_CHOICES, initial=3)

    def __init__(self, *args, **kwargs):
        super(SubscriptionCreationAdminForm, self).__init__(*args, **kwargs)
        start = self.fields['start']
        cw = Week.thisweek()
        choices = [str(w + cw.week) for w in Week.weeks_of_year(cw.year)]
        start.choices = zip(choices, choices)
        start.initial = cw+1

    def save(self, commit=True):
        subscription = super(SubscriptionCreationAdminForm, self).save(commit=False)
        bw = Week.fromstring(self.cleaned_data['start'])
        ew = Week.withdate( bw.day(1) + relativedelta(months=int(self.cleaned_data['duration'])) )
        subscription.end = ew
        if commit: subscription.save()
        return subscription

class SubscriptionAdminForm(SubscriptionBaseAdminForm):
    class Meta:
        model = models.Subscription
        fields = ('status', 'customer', 'size', 'criterias', 'quantity',)

    def clean_status(self):
        old_status = self.initial.get('status')
        status = self.cleaned_data.get('status')
        if old_status == 'v':
            raise forms.ValidationError(_('The status is already validated. It cannot be changed anymore.'))
        return status

class ExtentAdminForm(forms.ModelForm):
    class Meta:
        model = models.Extent

class DeliveryCreationAdminForm(forms.ModelForm):
    class Meta:
        model = models.Delivery

    def __init__(self, *args, **kwargs):
        super(DeliveryCreationAdminForm, self).__init__(*args, **kwargs)
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
        super(CreateForm, self).__init__(*args, **kwargs)
        start = self.fields['start']
        cw = Week.thisweek()
        choices = [str(w + cw.week) for w in Week.weeks_of_year(cw.year)]
        start.choices = zip(choices, choices)
        start.initial = cw+1

    def save(self, commit=True):
        subscription = super(CreateForm, self).save(commit=False)
        bw = Week.fromstring(self.cleaned_data['start'])
        ew = Week.withdate( bw.day(1) + relativedelta(months=int(self.cleaned_data['duration'])) )
        subscription.end = ew
        if commit: subscription.save()
        return subscription

class CreateForm1(forms.Form):
    size = forms.HiddenInput()
    frequency = forms.HiddenInput()
    duration = forms.HiddenInput()
    start = forms.HiddenInput()
    # products = forms.MultipleChoiceField(help_text=_('Use CTRL to select several products.'))
    # criterias = forms.MultipleChoiceField(help_text=_('Use CTRL to select several criterias.'))

    def __init__(self, *args, **kwargs):
        super(CreateForm1, self).__init__(*args, **kwargs)
        # start = self.fields['start']
        # cw = Week.thisweek()
        # choices = [str(w + cw.week) for w in Week.weeks_of_year(cw.year)]
        # start.choices = zip(choices, choices)
        # start.initial = cw+1
        # self.fields['products'].choices = [(product.id, product) for product in pm.Product.objects.all()]
        # self.fields['criterias'].choices = [(criteria.id, criteria) for criteria in cm.Criteria.objects.all()]

class CreateForm2(forms.Form):
    # extents = forms.MultipleHiddenInput()

    def __init__(self, *args, **kwargs):
        super(CreateForm2, self).__init__(*args, **kwargs)
