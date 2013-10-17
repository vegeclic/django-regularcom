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

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.contrib.formtools.wizard.views import WizardView, SessionWizardView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from customers import models as cm
from . import forms, models
import products.models as pm
import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week
import numpy as np

def get_products_tree(products, root_product=None, root_only=True):
    dict_ = {}
    for product in products:
        if product == root_product: continue
        if product.status != 'p': continue
        if not product.products_parent.all() or not root_only:
            dict_[product] = get_products_tree(product.products_children.all(), root_product=product, root_only=False)
    return dict_

class CatalogView(generic.ListView):
    model = models.Product
    template_name = 'suppliers/catalog.html'

    def get_queryset(self):
        products_tree = get_products_tree(pm.Product.objects.all())

        product_list = []

        def find_product(products_tree, product_pattern):
            for product, products in products_tree.items():
                if product.id == int(product_pattern): return products
                res = find_product(products, product_pattern)
                if res: return res
            return None

        def get_suppliers_products(products_tree):
            if not products_tree: return []
            product_list = []
            for product, products in products_tree.items():
                product_list += self.model.objects.filter(product=product)
                product_list += get_suppliers_products(products)
            return product_list

        if self.kwargs.get('product_id'):
            root_product = find_product(products_tree, self.kwargs.get('product_id'))
            product_list += get_suppliers_products(root_product)
        else:
            product_list += self.model.objects.all()

        paginator = Paginator(product_list, 24) # Show 24 products per page

        page = self.kwargs.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            products = paginator.page(paginator.num_pages)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'catalog'
        context['products_tree'] = get_products_tree(pm.Product.objects.all())
        if self.kwargs.get('product_id'):
            context['selected_product'] = pm.Product.objects.get(id=self.kwargs.get('product_id'))
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): return super().dispatch(*args, **kwargs)
