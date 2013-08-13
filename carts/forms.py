from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from . import models
import common.forms as cf
import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week
from pprint import pprint

class ThematicForm(cf.ModelFormWithImage):
    class Meta:
        model = models.Thematic

class ThematicCreationForm(forms.ModelForm):
    class Meta:
        model = models.Thematic
        exclude = ('main_image',)

class SizeForm(cf.ModelFormWithImage):
    class Meta:
        model = models.Size

class SizeCreationForm(forms.ModelForm):
    class Meta:
        model = models.Size
        exclude = ('main_image',)

class PriceForm(cf.ModelFormWithCurrency):
    class Meta:
        model = models.Price

class SubscriptionBaseForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(SubscriptionBaseForm, self).clean()
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

class SubscriptionCreationForm(SubscriptionBaseForm):
    class Meta:
        model = models.Subscription
        fields = ('status', 'customer', 'size', 'frequency', 'duration', 'start', 'criterias', 'quantity',)

    DURATION_CHOICES = (
        (1, _('1 month')),
        (3, _('3 months')),
        (6, _('6 months')),
        (9, _('9 months')),
        (12, _('1 year')),
    )
    duration = forms.ChoiceField(choices=DURATION_CHOICES, initial=3)

    def __init__(self, *args, **kwargs):
        super(SubscriptionCreationForm, self).__init__(*args, **kwargs)
        start = self.fields['start']
        cw = Week.thisweek()
        choices = [str(w + cw.week) for w in Week.weeks_of_year(cw.year)]
        start.choices = zip(choices, choices)
        start.initial = cw+1

    def save(self, commit=True):
        subscription = super(SubscriptionCreationForm, self).save(commit=False)
        bw = Week.fromstring(self.cleaned_data['start'])
        ew = Week.withdate( bw.day(1) + relativedelta(months=int(self.cleaned_data['duration'])) )
        subscription.end = ew
        if commit: subscription.save()
        return subscription

class SubscriptionForm(SubscriptionBaseForm):
    class Meta:
        model = models.Subscription
        fields = ('status', 'customer', 'size', 'criterias', 'quantity',)

    def clean_status(self):
        old_status = self.initial.get('status')
        status = self.cleaned_data.get('status')
        if old_status == 'v':
            raise forms.ValidationError(_('The status is already validated. It cannot be changed anymore.'))
        return status

class ExtentForm(forms.ModelForm):
    class Meta:
        model = models.Extent

class DeliveryCreationForm(forms.ModelForm):
    class Meta:
        model = models.Delivery

    def __init__(self, *args, **kwargs):
        super(DeliveryCreationForm, self).__init__(*args, **kwargs)
        date = self.fields['date']
        cw = Week.thisweek()
        choices = [str(w + cw.week) for w in Week.weeks_of_year(cw.year)]
        date.choices = zip(choices, choices)
        date.initial = cw+1

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = models.Delivery

class ContentForm(forms.ModelForm):
    class Meta:
        model = models.Content
