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
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from . import models
import common.models as cm
import common.forms as cf

class AccountCreationAdminForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    # password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    # password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput)

    class Meta:
        model = models.Account
        fields = ('email',)

    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
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
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class AccountCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        # 'password_mismatch': _("The two password fields didn't match."),
    }
    email = forms.EmailField(label=_("Email address"), max_length=255)
    # password1 = forms.CharField(label=_("Password"),
    #                             widget=forms.PasswordInput)
    # password2 = forms.CharField(label=_("Password confirmation"),
    #                             widget=forms.PasswordInput,
    #                             help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = models.Account
        fields = ("email",)

    def clean_email(self):
        # Since Account.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            models.Account._default_manager.get(email=email)
        except models.Account.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError(self.error_messages['password_mismatch'])
    #     return password2

    def save(self, commit=True):
        account = super().save(commit=False)
        # account.set_password(self.cleaned_data["password1"])
        if commit: account.save()
        return account

class AuthorForm(cf.ModelFormWithImage):
    class Meta:
        model = models.Author

class AuthorCreationForm(forms.ModelForm):
    class Meta:
        model = models.Author
        exclude = ('main_image',)
