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
from . import views, models, forms

urlpatterns = patterns('carts.views',
                       url(r'^subscriptions/$', views.SubscriptionView.as_view(), name='subscriptions'),
                       url(r'^subscriptions/(?P<subscription_id>\d+)/edit/$', views.SubscriptionUpdateView.as_view(), name='subscription_edit'),
                       url(r'^subscriptions/(?P<subscription_id>\d+)/deliveries/$', views.DeliveryView.as_view(), name='subscription_deliveries'),
                       url(r'^deliveries/$', views.DeliveryView.as_view(), name='deliveries'),
                       url(r'^subscriptions/(?P<subscription_id>\d+)/deliveries/(?P<delivery_id>\d+)/validate/$', views.DeliveryPaymentView.as_view(), name='subscription_delivery_validate'),
                       url(r'^create_custom/$', views.CreateWizard.as_view([forms.CreateForm1, forms.CreateForm2], condition_dict={'1': views.show_extent_form_condition}), name='create_custom'),
                       url(r'^create/thematic/$', views.ThematicListView.as_view(), name='create_thematic'),
                       url(r'^create/thematic/(?P<thematic_id>\d+)/$', views.CreateWizard.as_view([forms.CreateForm1, forms.CreateForm2], condition_dict={'1': views.show_extent_form_condition}), name='create_thematic_id'),
)
