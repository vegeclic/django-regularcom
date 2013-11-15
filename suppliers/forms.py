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
from django.utils.translation import ugettext_lazy as _
from modeltranslation.forms import TranslationModelForm
from . import models
import common.forms as cf
import common.models as cm
import products.models as pm

class SupplierForm(cf.ModelFormWithImage):
    class Meta:
        model = models.Supplier

class SupplierCreationForm(forms.ModelForm):
    class Meta:
        model = models.Supplier
        exclude = ('main_image',)

class PriceForm(cf.ModelFormWithCurrency):
    class Meta:
        model = models.Price

class ProductForm(TranslationModelForm):
    class Meta:
        model = models.Product

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

        # self.fields['product'].queryset = pm.Product.objects.order_by('name')
