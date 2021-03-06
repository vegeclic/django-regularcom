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
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
import common.models as cm

class Customer(models.Model):
    account = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(null=True, blank=True)
    main_address = models.OneToOneField('common.Address', null=True, blank=True, related_name='customer_main_address')
    shipping_address = models.OneToOneField('common.Address', null=True, blank=True, related_name='customer_shipping_address')
    billing_address = models.OneToOneField('common.Address', null=True, blank=True, related_name='customer_billing_address')
    relay_address = models.OneToOneField('common.Address', null=True, blank=True, related_name='customer_relay_address')
    addresses = generic.GenericRelation(cm.Address)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='customer_main_image')
    pro = models.BooleanField(_('pro'), default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return '%s%s' % (self.account.email, (' (%s)' % self.main_address.__unicode__()) if self.main_address else '')

    def get_shipping_address(self): return self.shipping_address if self.shipping_address else self.main_address

    def get_billing_address(self): return self.billing_address if self.billing_address else self.main_address

    def is_pro(self): return self.pro
