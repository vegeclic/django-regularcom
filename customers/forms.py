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

class MyRadioInput(forms.widgets.SubWidget):
    """
    An object used by RadioFieldRenderer that represents a single
    <input type='radio'>.
    """

    def __init__(self, name, value, attrs, choice, index):
        self.name, self.value = name, value
        self.attrs = attrs
        self.choice_value = forms.widgets.force_text(choice[0])
        self.choice_label = forms.widgets.force_text(choice[1])
        self.index = index

    def __str__(self):
        return self.render()

    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        if 'id' in self.attrs:
            label_for = forms.widgets.format_html(' for="{0}_{1}"', self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = forms.widgets.force_text(self.choice_label)
        return forms.widgets.format_html('<label class="btn btn-default btn-lg {0} {1}" {2}>{3} {4}</label>',
                                         'active' if self.is_checked() else '',
                                         'disabled' if 'disabled' in attrs else '',
                                         label_for, self.tag(), choice_label)

    def is_checked(self):
        return self.value == self.choice_value

    def tag(self):
        if 'id' in self.attrs:
            self.attrs['id'] = '%s_%s' % (self.attrs['id'], self.index)
        final_attrs = dict(self.attrs, type='radio', name=self.name, value=self.choice_value)
        if self.is_checked():
            final_attrs['checked'] = 'checked'
        return forms.widgets.format_html('<input{0} />', forms.widgets.flatatt(final_attrs))

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
        return forms.widgets.format_html('<div class="btn-group" data-toggle="buttons">\n{0}\n</div>', forms.widgets.format_html_join('\n', '{0}', [(forms.widgets.force_text(w),) for w in self]))

class SettingsForm(forms.ModelForm):
    class Meta:
        model = am.Account
        fields = ('newsletter',)

    newsletter = forms.ChoiceField(widget=forms.RadioSelect(renderer=MyRadioFieldRenderer), choices=am.NEWSLETTER_FREQUENCIES, initial='i')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        for field in ['newsletter']:
            self.fields[field].widget.attrs['class'] = 'radio-select'
