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
from . import views, models

urlpatterns = patterns('customers.views',
                       url(r'^$', views.CustomerView.as_view(), name='profile'),
                       url(r'^password_reset/$', views.PasswordResetView.as_view(), name='password_reset'),
                       url(r'^addresses/$', views.AddressListView.as_view(), name='addresses'),
                       url(r'^addresses/create/$', views.AddressCreateView.as_view(), name='address_create'),
                       url(r'^addresses/(?P<address_id>\d+)/edit/$', views.AddressUpdateView.as_view(), name='address_edit'),
                       url(r'^addresses/(?P<address_id>\d+)/remove/$', views.AddressDeleteView.as_view(), name='address_remove'),
                       url(r'^addresses/(?P<address_id>\d+)/define_as_main/$', views.AddressDefineAsMainView.as_view(), name='address_define_as_main'),
                       url(r'^addresses/(?P<address_id>\d+)/define_as_shipping/$', views.AddressDefineAsShippingView.as_view(), name='address_define_as_shipping'),
                       url(r'^addresses/(?P<address_id>\d+)/define_as_billing/$', views.AddressDefineAsBillingView.as_view(), name='address_define_as_billing'),
                       # url(r'^settings/$', views.SettingsView.as_view(), name='settings'),
)
