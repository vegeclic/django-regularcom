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

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, DetailView, ListView
from . import views, models, forms

urlpatterns = patterns('suppliers.views',
                       url(r'^catalog/$', views.CatalogGridView.as_view(), name='catalog'),
                       url(r'^catalog/grid/$', views.CatalogGridView.as_view(), name='catalog_grid'),
                       url(r'^catalog/list/$', views.CatalogListView.as_view(), name='catalog_list'),

                       url(r'^catalog/page/(?P<page>\d+)/$', views.CatalogGridView.as_view(), name='catalog_page'),
                       url(r'^catalog/grid/page/(?P<page>\d+)/$', views.CatalogGridView.as_view(), name='catalog_grid_page'),
                       url(r'^catalog/list/page/(?P<page>\d+)/$', views.CatalogListView.as_view(), name='catalog_list_page'),

                       url(r'^catalog/(?P<product_id>\d+)/$', views.CatalogGridView.as_view(), name='catalog_product_id'),
                       url(r'^catalog/grid/(?P<product_id>\d+)/$', views.CatalogGridView.as_view(), name='catalog_grid_product_id'),
                       url(r'^catalog/list/(?P<product_id>\d+)/$', views.CatalogListView.as_view(), name='catalog_list_product_id'),

                       url(r'^catalog/(?P<product_id>\d+)/(?P<slug>[\w-]+)/$', views.CatalogGridView.as_view(), name='catalog_product_id_slug'),
                       url(r'^catalog/grid/(?P<product_id>\d+)/(?P<slug>[\w-]+)/$', views.CatalogGridView.as_view(), name='catalog_grid_product_id_slug'),
                       url(r'^catalog/list/(?P<product_id>\d+)/(?P<slug>[\w-]+)/$', views.CatalogListView.as_view(), name='catalog_list_product_id_slug'),

                       url(r'^catalog/(?P<product_id>\d+)/page/(?P<page>\d+)/$', views.CatalogGridView.as_view(), name='catalog_product_id_page'),
                       url(r'^catalog/grid/(?P<product_id>\d+)/page/(?P<page>\d+)/$', views.CatalogGridView.as_view(), name='catalog_grid_product_id_page'),
                       url(r'^catalog/list/(?P<product_id>\d+)/page/(?P<page>\d+)/$', views.CatalogListView.as_view(), name='catalog_list_product_id_page'),

                       url(r'^catalog/(?P<product_id>\d+)/(?P<slug>[\w-]+)/page/(?P<page>\d+)/$', views.CatalogGridView.as_view(), name='catalog_product_id_slug_page'),
                       url(r'^catalog/grid/(?P<product_id>\d+)/(?P<slug>[\w-]+)/page/(?P<page>\d+)/$', views.CatalogGridView.as_view(), name='catalog_grid_product_id_slug_page'),
                       url(r'^catalog/list/(?P<product_id>\d+)/(?P<slug>[\w-]+)/page/(?P<page>\d+)/$', views.CatalogListView.as_view(), name='catalog_list_product_id_slug_page'),
)
