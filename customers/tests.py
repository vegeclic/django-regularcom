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

from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.core import mail
from . import models
import accounts.models as am
import common.models as cm

EMAIL_ADMIN, EMAIL, PASSWORD = 'admin@admin.xyz', 'john@smith.xyz', 'mypassword'

def create_customer(email, password=''):
    account = am.Account.objects.create_user(email)
    if password:
        account.set_password(password)
        account.save()
    return account.customer

def create_address(customer, first_name, last_name):
    return cm.Address.objects.create(content_type=ContentType.objects.get(model='customer'), object_id=customer.id, first_name=first_name, last_name=last_name)

def create_customer_with_main_address(email, first_name, last_name, password=''):
    customer = create_customer(email, password)
    customer.main_address = create_address(customer, first_name, last_name)
    customer.save()
    return customer

@override_settings(EMAIL_ADMIN=EMAIL_ADMIN)
class CustomerMethodTests(TestCase):
    def test_get_shipping_address_when_empty(self):
        """
        get_shipping_address() should return main_address for customers whose shipping_address is empty.
        """
        customer = create_customer_with_main_address(EMAIL, 'John', 'Smith')
        self.assertEqual(customer.get_shipping_address(), customer.main_address)

    def test_get_billing_address_when_empty(self):
        """
        get_billing_address() should return main_address for customers whose billing_address is empty.
        """
        customer = create_customer_with_main_address(EMAIL, 'John', 'Smith')
        self.assertEqual(customer.get_billing_address(), customer.main_address)

    def test_get_shipping_address_when_not_empty(self):
        """
        get_shipping_address() should return shipping_address for customers whose shipping_address is not empty.
        """
        customer = create_customer(EMAIL)
        customer.shipping_address = create_address(customer, 'Jojo', 'Smismi')
        customer.save()
        self.assertEqual(customer.get_shipping_address(), customer.shipping_address)

    def test_get_billing_address_when_not_empty(self):
        """
        get_billing_address() should return billing_address for customers whose billing_address is not empty.
        """
        customer = create_customer(EMAIL)
        customer.billing_address = create_address(customer, 'Jojo', 'Smismi')
        customer.save()
        self.assertEqual(customer.get_billing_address(), customer.billing_address)

    def test_is_pro_when_default_behavior(self):
        """
        is_pro() should return False for customers created with default behavior.
        """
        customer = create_customer(EMAIL)
        self.assertEqual(customer.is_pro(), False)

    def test_is_pro_when_customer_is_pro(self):
        """
        is_pro() should return True for customers created with the pro status.
        """
        customer = create_customer(EMAIL)
        customer.pro = True
        customer.save()
        self.assertEqual(customer.is_pro(), True)

@override_settings(EMAIL_ADMIN=EMAIL_ADMIN)
class CustomerDetailViewTests(TestCase):
    def test_detail_view_isequal_to_customer_object(self):
        """
        Check that context['object'] is equal to customer object.
        """
        customer = create_customer(EMAIL, PASSWORD)
        self.assertEqual(len(mail.outbox), 1)
        self.client.login(username=EMAIL, password=PASSWORD)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.context['object'], customer)

    def test_detail_view_get_context_data(self):
        """
        get_context_data() should set the following keys with values.
        """
        customer = create_customer(EMAIL, PASSWORD)
        self.client.login(username=EMAIL, password=PASSWORD)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.context['section'], 'customers')
        self.assertEqual(response.context['sub_section'], 'profile')

    def test_detail_view_without_addresses(self):
        """
        Ensure that the customer addresses are unset.
        """
        customer = create_customer(EMAIL, PASSWORD)
        self.assertEqual(len(mail.outbox), 1)
        self.client.login(username=EMAIL, password=PASSWORD)
        response = self.client.get(reverse('profile'))
        obj = response.context['object']
        self.assertIsNone(obj.main_address)
        self.assertIsNone(obj.shipping_address)
        self.assertIsNone(obj.billing_address)

@override_settings(EMAIL_ADMIN=EMAIL_ADMIN)
class AddressListViewTests(TestCase):
    def test_list_view_get_context_data(self):
        """
        get_context_data() should set the following keys with values.
        """
        customer = create_customer(EMAIL, PASSWORD)
        self.client.login(username=EMAIL, password=PASSWORD)
        response = self.client.get(reverse('addresses'))
        self.assertEqual(response.context['section'], 'customers')
        self.assertEqual(response.context['sub_section'], 'addresses')

    def test_list_view_get_queryset(self):
        """
        get_queryset() should return a queryset of address list.
        """
        customer = create_customer_with_main_address(EMAIL, 'John', 'Smith', password=PASSWORD)
        self.client.login(username=EMAIL, password=PASSWORD)
        response = self.client.get(reverse('addresses'))
        self.assertQuerysetEqual(response.context['object_list'], ['<Address: Address object>',])

    def test_list_view_login_required(self):
        response = self.client.get(reverse('addresses'))
        self.assertRedirects(response, 'accounts/login/?next=/customers/addresses/')

@override_settings(EMAIL_ADMIN=EMAIL_ADMIN)
class AddressCreateViewTests(TestCase):
    def test_create_view_create_an_address(self):
        customer = create_customer(EMAIL, PASSWORD)
        self.client.login(username=EMAIL, password=PASSWORD)

        response = self.client.get(reverse('addresses'))
        self.assertQuerysetEqual(response.context['object_list'], [])

        self.client.post(reverse('address_create'))

        response = self.client.get(reverse('addresses'))
        self.assertQuerysetEqual(response.context['object_list'], ['<Address: Address object>',])

    def test_create_view_login_required(self):
        response = self.client.post(reverse('address_create'))
        self.assertRedirects(response, 'accounts/login/?next=/customers/addresses/create/')

@override_settings(EMAIL_ADMIN=EMAIL_ADMIN)
class AddressUpdateViewTests(TestCase):
    def test_update_view_edit_an_address(self):
        customer = create_customer_with_main_address(EMAIL, 'John', 'Smith', password=PASSWORD)
        self.client.login(username=EMAIL, password=PASSWORD)
        response = self.client.post(reverse('address_edit', args=(customer.main_address.pk,)), {'first_name': 'Jean', 'last_name': 'Dupont'})
        customer = models.Customer.objects.get(id=customer.id)
        self.assertEqual(customer.main_address.__unicode__(), 'Jean Dupont')
