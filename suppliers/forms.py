from django import forms
from . import models
import common.forms as cf

class SupplierForm(cf.ModelFormWithImage):
    class Meta:
        model = models.Supplier

class SupplierCreationForm(forms.ModelForm):
    class Meta:
        model = models.Supplier
        exclude = ('main_image',)

class ProductForm(cf.ModelFormWithImage):
    class Meta:
        model = models.Product

class ProductCreationForm(forms.ModelForm):
    class Meta:
        model = models.Product
        exclude = ('main_image',)
