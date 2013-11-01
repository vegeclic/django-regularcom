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
from django.core.cache import cache
import hvad
from customers import models as cm
from . import forms, models
import products.models as pm
import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week
import numpy as np

def get_products_tree(products, root_product=None, root_only=True):
    dict_ = {}
    for product in products.language('fr').prefetch_related('products_parent', 'products_children').select_related('main_image').order_by('name'):
        if product == root_product: continue
        if product.status != 'p': continue
        if not product.products_parent.exists() or not root_only:
            dict_[product] = get_products_tree(product.products_children, root_product=product, root_only=False)
    return dict_

class CatalogView(generic.ListView):
    model = models.Product
    template_name = 'suppliers/catalog.html'

    def get_queryset(self):
        products_tree = cache.get('products_tree') or get_products_tree(pm.Product.objects)
        if not cache.get('products_tree'): cache.set('products_tree', products_tree)

        def find_product(products_tree, product_pattern):
            for product, products in products_tree.items():
                if product.id == int(product_pattern): return {product: products}
                res = find_product(products, product_pattern)
                if res: return res
            return None

        def products_tree_to_list(products_tree):
            if not products_tree: return []
            __list = []
            for product, products in products_tree.items():
                __list.append(product)
                __list += products_tree_to_list(products)
            return __list

        def compute_degressive_price(product_list):
            for p in product_list: p.degressive_price = p.price().degressive_price(26)

        products_query = self.model.objects
        if self.kwargs.get('product_id'):
            root_product = find_product(products_tree, self.kwargs.get('product_id'))
            products_query = products_query.filter(product__in=products_tree_to_list(root_product))

        products_query = products_query.select_related('price', 'main_image', 'price__currency', 'price__tax').prefetch_related('criterias', 'suppliers')

        paginator = Paginator(products_query, 24)

        page = self.kwargs.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        compute_degressive_price(products.object_list)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'catalog'

        context['products_tree'] = cache.get('products_tree') or get_products_tree(pm.Product.objects)
        if not cache.get('products_tree'): cache.set('products_tree', context['products_tree'])

        if self.kwargs.get('product_id'):
            context['selected_product'] = pm.Product.objects.get(id=self.kwargs.get('product_id'))

            def get_product_path(products_tree, product_pattern, path=()):
                for product, products in products_tree.items():
                    if product == product_pattern: return path+(product,)
                    res = get_product_path(products, product_pattern, path+(product,))
                    if res: return res
                return None

            context['product_path'] = get_product_path(context['products_tree'], context['selected_product'])

        return context

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs): return super().dispatch(*args, **kwargs)

class CatalogGridView(CatalogView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = 'grid'
        return context

class CatalogListView(CatalogView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = 'list'
        return context
