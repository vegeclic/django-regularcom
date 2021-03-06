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

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
import datetime
from . import models
import common.forms as cf
import carts.forms as ctf

class WalletAdminForm(cf.ModelFormWithCurrency):
    class Meta:
        model = models.Wallet

class CreditCreationAdminForm(cf.ModelFormWithCurrency):
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

class WithdrawCreationAdminForm(cf.ModelFormWithCurrency):
    class Meta:
        model = models.Withdraw
        fields = ('wallet', 'payment_type', 'amount', 'currency',)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError(_('The amount must be positive.'))
        return amount

class CreditAdminForm(cf.ModelFormWithCurrency):
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

class WithdrawAdminForm(cf.ModelFormWithCurrency):
    class Meta:
        model = models.Withdraw
        fields = ('status', 'wallet', 'payment_type', 'amount', 'currency',)

    def clean_status(self):
        old_status = self.initial.get('status')
        status = self.cleaned_data.get('status')
        if old_status == 'v':
            raise forms.ValidationError(_('The status is already validated. It cannot be changed anymore.'))
        return status

class HistoryCreationAdminForm(forms.ModelForm):
    class Meta:
        model = models.History
        # fields = ('wallet', 'content_type', 'amount',)

class HistoryAdminForm(forms.ModelForm):
    class Meta:
        model = models.History
        # fields = ('site', 'name', 'content_type', 'object_id',)

    object_id = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        content_type = self.initial.get('content_type')
        object_id = self.initial.get('object_id')
        object_id_field = self.fields.get('object_id')
        object_id_field.choices = [(o.id, o) for o in ContentType.objects.get(pk=content_type).get_all_objects_for_this_type()]
        object_id_field.initial = object_id

class SettingsForm(cf.ModelFormWithCurrency):
    class Meta:
        model = models.Wallet
        exclude = ('customer', 'balance',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ['rib', 'paypal', 'bitcoin']:
            self.fields[field].widget = w = forms.Textarea()
            w.attrs['rows'] = 3

        for field in self.fields:
            print(field)
            self.fields[field].widget.attrs['class'] = 'form-control'

class CreditForm(cf.ModelFormWithCurrency):
    class Meta:
        model = models.Credit
        fields = ('payment_type', 'amount',)
        widgets = {
            'payment_type': forms.RadioSelect(renderer=ctf.MyRadioFieldRenderer),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields.get('payment_date').widget.attrs = {'class': 'form-control'}
        self.fields.get('payment_type').widget.attrs['class'] = 'radio-select'

    def clean_amount(self):
        amount = abs(self.cleaned_data.get('amount'))
        if not amount:
            raise forms.ValidationError(_('The amount must be positive.'))
        return amount

    # def clean_payment_date(self):
    #     payment_type = self.cleaned_data.get('payment_type')
    #     payment_date = self.cleaned_data.get('payment_date')
    #     if payment_date and payment_type != 'c':
    #         raise forms.ValidationError(_('The payment date is only needed for payment with cheque.'))
    #     return payment_date

class WithdrawForm(cf.ModelFormWithCurrency):
    class Meta:
        model = models.Withdraw
        fields = ('payment_type', 'amount',)
        widgets = {
            'payment_type': forms.RadioSelect(renderer=ctf.MyRadioFieldRenderer),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('payment_type').widget.attrs['class'] = 'radio-select'

    def clean_amount(self):
        amount = abs(self.cleaned_data.get('amount'))
        if not amount:
            raise forms.ValidationError(_('The amount must be positive.'))
        return amount
