from django import forms
from common.models import Address, Image

class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)

        for field in ['main_address', 'shipping_address', 'billing_address']:
            if 'instance' in kwargs:
                self.fields[field].queryset = Address.objects.filter(customer=kwargs['instance'])
            else:
                self.fields[field].queryset = Address.objects.none()

        # if 'instance' in kwargs:
        #     self.fields['main_image'].queryset = Image.objects.filter(object_id=kwargs['instance'].id)
        # else:
        #     self.fields['main_image'].queryset = Image.objects.none()
