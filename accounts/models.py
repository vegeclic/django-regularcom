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
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
import common.models as cm
import customers.models as csm
import wallets.models as wm
import mailbox.models as mm

class AccountManager(BaseUserManager):
    def create_user(self, email):
        """
        Creates and saves a User with the given email and password.
        """
        if not email: raise ValueError('Users must have an email address')

        account = self.model(email=AccountManager.normalize_email(email).lower())
        password = self.make_random_password()
        account.set_password(password)
        account.save(using=self._db)

        customer = csm.Customer.objects.create(account=account)
        wallet = wm.Wallet.objects.create(customer=customer, balance=settings.BALANCE_INIT, target_currency=cm.Parameter.objects.get(name='default currency').content_object)

        message = mm.Message.objects.create_message(mail_only=True, participants=[customer], subject=_('Welcome to Végéclic'), body=_(
"""Hi there,

We are pleased to see you among us on the new website of Végéclic.

You can authenticate to your account with the following information:

email: %(email)s
password: %(password)s

or just click on the link bellow to be directly connected (without authentication-step):

http://www.vegeclic.fr/accounts/email/%(email)s/password/%(password)s/

Ready ? Go to the "carts" section in order to create a new subscription. It is quite simple!

Best regards,
Végéclic.
"""
        ) % {'email': account.email, 'password': password})

        return account

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        account = self.create_user(email, password=password)
        account.is_admin = True
        account.save(using=self._db)
        return account

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name=_('email address'), max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_absolute_url(self):
        return "/accounts/%s/" % urlquote(self.email)

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Author(models.Model):
    account = models.OneToOneField(Account, verbose_name=_('account'))
    name = models.CharField(_('name'), max_length=30, blank=True)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+', verbose_name=_('main image'))

    def __unicode__(self): return self.name
