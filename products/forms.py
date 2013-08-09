from django import forms
from . import models
import common.forms as cf

class CategoryForm(cf.ModelFormWithImage):
    class Meta:
        model = models.Category

class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = models.Category
        exclude = ('main_image',)

class ProductForm(cf.ModelFormWithImage):
    class Meta:
        model = models.Product

class ProductCreationForm(forms.ModelForm):
    class Meta:
        model = models.Product
        exclude = ('main_image',)
