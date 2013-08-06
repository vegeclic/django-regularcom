from django import forms
from common.models import Image

class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)

        if 'instance' in kwargs:
            self.fields['main_image'].queryset = Image.objects.filter(object_id=kwargs['instance'].id)
        else:
            self.fields['main_image'].queryset = Image.objects.none()

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        if 'instance' in kwargs:
            self.fields['main_image'].queryset = Image.objects.filter(object_id=kwargs['instance'].id)
        else:
            self.fields['main_image'].queryset = Image.objects.none()
