from django import forms
from . import models

class ModelFormWithImage(forms.ModelForm):
    main_image = 'main_image'

    def __init__(self, *args, **kwargs):
        super(ModelFormWithImage, self).__init__(*args, **kwargs)

        if 'instance' in kwargs:
            self.fields[self.main_image].queryset = models.Image.objects.filter(object_id=kwargs['instance'].id)

class ParameterForm(forms.ModelForm):
    class Meta:
        model = models.Parameter
        fields = ('site', 'name', 'object_id',)

class ParameterCreationForm(forms.ModelForm):
    class Meta:
        model = models.Parameter
        fields = ('site', 'name', 'content_type',)
