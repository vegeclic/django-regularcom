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

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
import django.contrib.auth.decorators as ad
from django.utils.decorators import method_decorator
import suppliers.views as sw

def pro_required(function=None, redirect_field_name=ad.REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is a pro customer, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = ad.user_passes_test(
        lambda u: u.customer.is_pro(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

class HomeView(generic.TemplateView):
    template_name = 'pro/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'pro'
        return context

class CatalogGridView(sw.CatalogView):
    template_name = "pro/catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = 'grid'
        return context

    @method_decorator(pro_required)
    def dispatch(self, *args, **kwargs): return super().dispatch(*args, **kwargs)

class CatalogListView(sw.CatalogView):
    template_name = "pro/catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = 'list'
        return context

    @method_decorator(pro_required)
    def dispatch(self, *args, **kwargs): return super().dispatch(*args, **kwargs)
