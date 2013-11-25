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
import common.models as cm
import common.forms as cf
import carts.forms as ctf
import accounts.models as am
from . import models

class CustomerCreationForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        exclude = ('main_address', 'shipping_address', 'billing_address', 'relay_address', 'main_image',)

class CustomerForm(cf.ModelFormWithImage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ['main_address', 'shipping_address', 'billing_address', 'relay_address']:
            if 'instance' in kwargs:
                self.fields[field].queryset = cm.Address.objects.filter(object_id=kwargs['instance'].id)

class AddressCreateForm(forms.ModelForm):
    class Meta:
        model = cm.Address
        exclude = ('content_type', 'object_id',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = cm.Address
        exclude = ('content_type', 'object_id',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

class SettingsForm(forms.ModelForm):
    class Meta:
        model = am.Account
        fields = ('newsletter',)

    newsletter = forms.ChoiceField(widget=forms.RadioSelect(renderer=ctf.MyRadioFieldRenderer), choices=am.NEWSLETTER_FREQUENCIES, initial='i')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        for field in ['newsletter']:
            self.fields[field].widget.attrs['class'] = 'radio-select'
