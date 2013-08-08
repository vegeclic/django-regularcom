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
