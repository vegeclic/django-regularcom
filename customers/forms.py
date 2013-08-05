from django import forms
from .models import Address

class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['main_address'].queryset = Address.objects.filter(account=kwargs['instance'].account)
            self.fields['shipping_address'].queryset = Address.objects.filter(account=kwargs['instance'].account)
            self.fields['billing_address'].queryset = Address.objects.filter(account=kwargs['instance'].account)
