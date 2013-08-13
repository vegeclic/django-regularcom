from django import forms
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from . import models

class ModelFormWithImage(forms.ModelForm):
    main_image = 'main_image'

    def __init__(self, *args, **kwargs):
        super(ModelFormWithImage, self).__init__(*args, **kwargs)

        if 'instance' in kwargs:
            self.fields[self.main_image].queryset = models.Image.objects.filter(object_id=kwargs['instance'].id)

class ModelFormWithCurrency(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelFormWithCurrency, self).__init__(*args, **kwargs)

        if 'instance' not in kwargs:
            self.initial['currency'] = models.Parameter.objects.get(name='default currency').object_id

class ParameterForm(forms.ModelForm):
    class Meta:
        model = models.Parameter
        fields = ('site', 'name', 'content_type', 'object_id',)

    object_id = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(ParameterForm, self).__init__(*args, **kwargs)
        content_type = self.initial.get('content_type')
        object_id = self.initial.get('object_id')
        object_id_field = self.fields.get('object_id')
        object_id_field.choices = [(o.id, o) for o in ContentType.objects.get(pk=content_type).get_all_objects_for_this_type()]
        object_id_field.initial = object_id

class ParameterCreationForm(forms.ModelForm):
    class Meta:
        model = models.Parameter
        fields = ('site', 'name', 'content_type',)
