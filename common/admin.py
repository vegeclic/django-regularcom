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

from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from . import models, forms

class MyModelAdmin(admin.ModelAdmin):
    add_form = None

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during creation
        """
        defaults = {}
        if obj is None:
            defaults.update({
                'form': self.add_form if self.add_form else self.form,
            })
        defaults.update(kwargs)
        return super(MyModelAdmin, self).get_form(request, obj, **defaults)

class LimitedAdminInlineMixin(object):
    """
    InlineAdmin mixin limiting the selection of related items according to
    criteria which can depend on the current parent object being edited.

    A typical use case would be selecting a subset of related items from
    other inlines, ie. images, to have some relation to other inlines.

    Use as follows::

        class MyInline(LimitedAdminInlineMixin, admin.TabularInline):
            def get_filters(self, obj):
                return (('<field_name>', dict(<filters>)),)

    https://gist.github.com/dokterbob/828117
    """

    @staticmethod
    def limit_inline_choices(formset, field, empty=False, **filters):
        """
        This function fetches the queryset with available choices for a given
        `field` and filters it based on the criteria specified in filters,
        unless `empty=True`. In this case, no choices will be made available.
        """
        assert field in formset.form.base_fields

        qs = formset.form.base_fields[field].queryset
        if empty:
            formset.form.base_fields[field].queryset = qs.none()
        else:
            qs = qs.filter(**filters)

            formset.form.base_fields[field].queryset = qs

    def get_formset(self, request, obj=None, **kwargs):
        """
        Make sure we can only select variations that relate to the current
        item.
        """
        formset = \
            super(LimitedAdminInlineMixin, self).get_formset(request,
                                                             obj,
                                                             **kwargs)

        for (field, filters) in self.get_filters(obj):
            if obj:
                self.limit_inline_choices(formset, field, **filters)
            else:
                self.limit_inline_choices(formset, field, empty=True)

        return formset

    def get_filters(self, obj):
        """
        Return filters for the specified fields. Filters should be in the
        following format::

            (('field_name', {'categories': obj}), ...)

        For this to work, we should either override `get_filters` in a
        subclass or define a `filters` property with the same syntax as this
        one.
        """
        return getattr(self, 'filters', ())

class CountryAdmin(admin.ModelAdmin):
    fieldsets = []
    list_display = ('name',)

admin.site.register(models.Country, CountryAdmin)

class CurrencyAdmin(MyModelAdmin):
    fieldsets = []
    list_display = ('name', 'symbol', 'exchange_rate',)

admin.site.register(models.Currency, CurrencyAdmin)

class AddressInline(generic.GenericStackedInline):
    model = models.Address
    extra = 1

class ImageInline(generic.GenericTabularInline):
    model = models.Image
    extra = 1

class CriteriaAdmin(MyModelAdmin):
    fieldsets = []
    list_display = ('name',)

admin.site.register(models.Criteria, CriteriaAdmin)

class ParameterAdmin(MyModelAdmin):
    form = forms.ParameterForm
    add_form = forms.ParameterCreationForm
    fieldsets = []
    list_display = ('site', 'content_type', 'name', 'value',)

    def value(self, obj): return obj.content_object

admin.site.register(models.Parameter, ParameterAdmin)
