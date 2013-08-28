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

urlpatterns = patterns('carts.views',
                       url(r'^subscriptions/$', views.SubscriptionView.as_view(), name='subscriptions'),
                       url(r'^deliveries/(?P<pk>\d+)/$', views.DeliveryView.as_view(), name='deliveries'),
                       url(r'^deliveries/$', views.DeliveryView.as_view(), name='deliveries'),
                       url(r'^create/$', views.CreateView.as_view(), name='create'),
)
