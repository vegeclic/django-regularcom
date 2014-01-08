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
from . import models
import accounts.models as am
import common.models as cm

def create_customer(email):
    account, account_created = am.Account.objects.get_or_create(email=email)
    customer, customer_created = models.Customer.objects.get_or_create(account=account)
    return customer

def create_address(customer, first_name, last_name):
    return cm.Address.objects.create(content_type=ContentType.objects.get(model='customer'), object_id=customer.id, first_name=first_name, last_name=last_name)

def create_customer_with_main_address(email, first_name, last_name):
    customer = create_customer(email)
    customer.main_address = create_address(customer, first_name, last_name)
    customer.save()
    return customer

class CustomerMethodTests(TestCase):
    def test_get_shipping_address_when_empty(self):
        """
        get_shipping_address() should return main_address for customers whose shipping_address is empty.
        """
        customer = create_customer_with_main_address('john@smith.xyz', 'John', 'Smith')
        self.assertEqual(customer.get_shipping_address(), customer.main_address)

    def test_get_billing_address_when_empty(self):
        """
        get_billing_address() should return main_address for customers whose billing_address is empty.
        """
        customer = create_customer_with_main_address('john@smith.xyz', 'John', 'Smith')
        self.assertEqual(customer.get_billing_address(), customer.main_address)

    def test_get_shipping_address_when_not_empty(self):
        """
        get_shipping_address() should return shipping_address for customers whose shipping_address is not empty.
        """
        customer = create_customer('john@smith.xyz')
        customer.shipping_address = create_address(customer, 'Jojo', 'Smismi')
        customer.save()
        self.assertEqual(customer.get_shipping_address(), customer.shipping_address)

    def test_get_billing_address_when_not_empty(self):
        """
        get_billing_address() should return billing_address for customers whose billing_address is not empty.
        """
        customer = create_customer('john@smith.xyz')
        customer.billing_address = create_address(customer, 'Jojo', 'Smismi')
        customer.save()
        self.assertEqual(customer.get_billing_address(), customer.billing_address)

    def test_is_pro_when_default_behavior(self):
        """
        is_pro() should return False for customers created with default behavior.
        """
        customer = create_customer('john@smith.xyz')
        self.assertEqual(customer.is_pro(), False)

    def test_is_pro_when_customer_is_pro(self):
        """
        is_pro() should return True for customers created with the pro status.
        """
        customer = create_customer('john@smith.xyz')
        customer.pro = True
        customer.save()
        self.assertEqual(customer.is_pro(), True)
