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

from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from . import models
import common.models as cm
import common.forms as cf

class AccountCreationAdminForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    class Meta:
        model = models.Account
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            models.Account._default_manager.get(email=email)
        except models.Account.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def save(self, commit=True):
        account = super().save(commit=False)
        account.set_password(models.Account.objects.make_random_password())
        if commit: account.save()
        return account

class AccountChangeAdminForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=_('Password'))

    class Meta:
        model = models.Account

    def clean_password(self):
        return self.initial["password"]

class AccountCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
    }
    email = forms.EmailField(label=_("Email address"), max_length=255)

    class Meta:
        model = models.Account
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        print(email)
        try:
            models.Account._default_manager.get(email=email)
        except models.Account.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def save(self, commit=True):
        account = super().save(commit=False)
        if commit: account.save()
        return account

class AccountAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        return self.cleaned_data.get('username').lower()

class AuthorForm(cf.ModelFormWithImage):
    class Meta:
        model = models.Author

class AuthorCreationForm(forms.ModelForm):
    class Meta:
        model = models.Author
        exclude = ('main_image',)

class PasswordResetForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        email_attrs = self.fields.get('email').widget.attrs
        email_attrs['class'] = 'form-control'
        email_attrs['placeholder'] = _('Email address')
