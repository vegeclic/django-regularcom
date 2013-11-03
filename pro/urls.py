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

from django.conf.urls.defaults import *
from django.views.generic import TemplateView, DetailView, ListView
from . import views

urlpatterns = patterns('pro.views',
                       url(r'^$', views.HomeView.as_view(), name='pro_home'),
                       url(r'^wholesaler/$', views.WholesalerView.as_view(), name='pro_wholesaler'),
                       url(r'^partners/$', views.PartnersView.as_view(), name='pro_partners'),

                       url(r'^catalog/$', views.CatalogGridView.as_view(), name='pro_catalog'),
                       url(r'^catalog/grid/$', views.CatalogGridView.as_view(), name='pro_catalog_grid'),
                       url(r'^catalog/list/$', views.CatalogListView.as_view(), name='pro_catalog_list'),

                       url(r'^catalog/page/(?P<page>\d+)/$', views.CatalogGridView.as_view(), name='pro_catalog_page'),
                       url(r'^catalog/grid/page/(?P<page>\d+)/$', views.CatalogGridView.as_view(), name='pro_catalog_grid_page'),
                       url(r'^catalog/list/page/(?P<page>\d+)/$', views.CatalogListView.as_view(), name='pro_catalog_list_page'),

                       url(r'^catalog/(?P<product_id>\d+)/$', views.CatalogGridView.as_view(), name='pro_catalog_product_id'),
                       url(r'^catalog/grid/(?P<product_id>\d+)/$', views.CatalogGridView.as_view(), name='pro_catalog_grid_product_id'),
                       url(r'^catalog/list/(?P<product_id>\d+)/$', views.CatalogListView.as_view(), name='pro_catalog_list_product_id'),

                       url(r'^catalog/(?P<product_id>\d+)/page/(?P<page>\d+)/$', views.CatalogGridView.as_view(), name='pro_catalog_product_id_page'),
                       url(r'^catalog/grid/(?P<product_id>\d+)/page/(?P<page>\d+)/$', views.CatalogGridView.as_view(), name='pro_catalog_grid_product_id_page'),
                       url(r'^catalog/list/(?P<product_id>\d+)/page/(?P<page>\d+)/$', views.CatalogListView.as_view(), name='pro_catalog_list_product_id_page'),
)
