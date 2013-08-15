from django import forms
from hvad.forms import TranslatableModelForm
from . import models
import common.forms as cf
import common.models as cm

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
