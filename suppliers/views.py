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
from django.db.models import Q
from customers import models as cm
from . import forms, models
import products.models as pm
import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week
import numpy as np

def get_products_tree(products, root_product=None, root_only=True):
    __list = []
    for product in products.order_by('name').prefetch_related('products_parent', 'products_children').select_related('main_image').filter(status='p'):
        if product == root_product: continue
        if not product.products_parent.exists() or not root_only:
            __list.append((product, get_products_tree(product.products_children, root_product=product, root_only=False)))
    return __list

def find_product(products_tree, product_pattern):
    for product, products in products_tree:
        if product.id == int(product_pattern): return [(product, products)]
        res = find_product(products, product_pattern)
        if res: return res
    return None

def products_tree_to_list(products_tree):
    if not products_tree: return []
    __list = []
    for product, products in products_tree:
        __list.append(product)
        __list += products_tree_to_list(products)
    return __list

def compute_degressive_price(product_list):
    for p in product_list: p.degressive_price = p.main_price.degressive_price(26)

class CatalogView(generic.ListView):
    model = models.Product
    template_name = 'suppliers/catalog.html'

    def get_queryset(self):
        products_tree = cache.get('products_tree') or get_products_tree(pm.Product.objects)
        if not cache.get('products_tree'): cache.set('products_tree', products_tree)

        products_query = self.model.objects.filter(status='p')

        search = self.request.GET.get('search')
        if search:
            if search[0] == '#':
                search_id = None
                try: search_id = int(search[1:])
                except: pass
                products_query = products_query.filter(id=search_id)
            else:
                search_id = None
                try: search_id = int(search)
                except: pass
                products_query = products_query.filter(Q(id=search_id) | Q(name__icontains=search) | Q(slug__icontains=search) | Q(body__icontains=search))

        if self.kwargs.get('product_id'):
            root_product = find_product(products_tree, self.kwargs.get('product_id'))
            products_query = products_query.filter(product__in=products_tree_to_list(root_product))

        products_query = products_query.select_related('main_image', 'main_price', 'main_price__currency', 'main_price__tax', 'main_price__supplier').prefetch_related('criterias', 'suppliers').order_by('-date_created')

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
                for product, products in products_tree:
                    if product == product_pattern: return path+(product,)
                    res = get_product_path(products, product_pattern, path+(product,))
                    if res: return res
                return None

            context['product_path'] = get_product_path(context['products_tree'], context['selected_product'])

        if self.request.GET.get('search'):
            context['search'] = self.request.GET.get('search')

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
