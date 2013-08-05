from django import forms
from .models import Price

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['prices'].queryset = Price.objects.filter(product=kwargs['instance'])
