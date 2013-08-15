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
from . import models

class CustomerCreationForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        exclude = ('main_address', 'shipping_address', 'billing_address', 'main_image',)

class CustomerForm(cf.ModelFormWithImage):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)

        for field in ['main_address', 'shipping_address', 'billing_address']:
            if 'instance' in kwargs:
                self.fields[field].queryset = cm.Address.objects.filter(object_id=kwargs['instance'].id)
