from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
import datetime
from . import models
import common.forms as cf

class WalletForm(cf.ModelFormWithCurrency):
    class Meta:
        model = models.Wallet

class CreditCreationForm(cf.ModelFormWithCurrency):
    class Meta:
        model = models.Credit
        fields = ('wallet', 'payment_type', 'amount', 'currency', 'payment_date',)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError(_('The amount must be positive.'))
        return amount

    def clean_payment_date(self):
        payment_type = self.cleaned_data.get('payment_type')
        payment_date = self.cleaned_data.get('payment_date')
        if payment_date and payment_type != 'c':
            raise forms.ValidationError(_('The payment date is only needed for payment with cheque.'))
        return payment_date

class CreditForm(cf.ModelFormWithCurrency):
    class Meta:
        model = models.Credit
        fields = ('status', 'wallet', 'payment_type', 'amount', 'currency', 'payment_date',)

    def clean_payment_date(self):
        status = self.cleaned_data.get('status')
        payment_type = self.cleaned_data.get('payment_type')
        payment_date = self.cleaned_data.get('payment_date')
        if status == 'v' and payment_type == 'c' and payment_date:
            if datetime.date.today() < payment_date:
                raise forms.ValidationError(_('The payment date is not reached yet.'))
        return payment_date

    def clean_status(self):
        old_status = self.initial.get('status')
        status = self.cleaned_data.get('status')
        if old_status == 'v':
            raise forms.ValidationError(_('The status is already validated. It cannot be changed anymore.'))
        return status

class HistoryCreationForm(forms.ModelForm):
    class Meta:
        model = models.History
        # fields = ('wallet', 'content_type', 'amount',)

class HistoryForm(forms.ModelForm):
    class Meta:
        model = models.History
        # fields = ('site', 'name', 'content_type', 'object_id',)

    object_id = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(HistoryForm, self).__init__(*args, **kwargs)
        content_type = self.initial.get('content_type')
        object_id = self.initial.get('object_id')
        object_id_field = self.fields.get('object_id')
        object_id_field.choices = [(o.id, o) for o in ContentType.objects.get(pk=content_type).get_all_objects_for_this_type()]
        object_id_field.initial = object_id
