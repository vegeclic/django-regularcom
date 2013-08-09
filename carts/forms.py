from django import forms
from . import models
import common.forms as cf
import datetime

class ThematicForm(cf.ModelFormWithImage):
    class Meta:
        model = models.Thematic

class ThematicCreationForm(forms.ModelForm):
    class Meta:
        model = models.Thematic
        exclude = ('main_image',)

class SizeForm(cf.ModelFormWithImage):
    class Meta:
        model = models.Size

class SizeCreationForm(forms.ModelForm):
    class Meta:
        model = models.Size
        exclude = ('main_image',)

class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order

    # start_period = forms.DateField(required=False, input_formats=('%W/%Y',))
