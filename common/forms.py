#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# Authors:
# Caner Candan <caner@candan.fr>, http://caner.candan.fr
# Geraldine Starke <geraldine@starke.fr>, http://www.vegeclic.fr
#

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
