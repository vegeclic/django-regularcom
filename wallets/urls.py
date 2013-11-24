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
from . import views, models

urlpatterns = patterns('wallets.views',
                       url(r'^$', views.BalanceView.as_view(), name='balance'),
                       url(r'^histories/page/(?P<page>\d+)/$', views.HistoryView.as_view(), name='histories'),
                       url(r'^credit_requests/page/(?P<page>\d+)/$', views.CreditRequestView.as_view(), name='credit_requests'),
                       url(r'^credit_requests/(?P<credit_id>\d+)/cancel/$', views.CreditCancelView.as_view(), name='credit_request_cancel'),
                       url(r'^withdraw_requests/page/(?P<page>\d+)/$', views.WithdrawRequestView.as_view(), name='withdraw_requests'),
                       url(r'^withdraw_requests/(?P<withdraw_id>\d+)/cancel/$', views.WithdrawCancelView.as_view(), name='withdraw_request_cancel'),
                       url(r'^credit/$', views.CreditView.as_view(), name='credit'),
                       url(r'^withdraw/$', views.WithdrawView.as_view(), name='withdraw'),
                       url(r'^settings/$', views.SettingsView.as_view(), name='settings'),
)
