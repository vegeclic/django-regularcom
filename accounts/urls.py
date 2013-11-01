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
from django.views.generic import TemplateView
from . import views, models

urlpatterns = patterns('accounts.views',
                       url(r'^login/$', 'login', name='login'),
                       url(r'^login/email/(?P<email>\S+)/password/(?P<password>\S+)/$', 'login_link', name='login_link'),
                       url(r'^logout/$', 'logout', name='logout'),
                       url(r'^profile/$', views.AccountView.as_view(), name='profile'),
                       url(r'^account_password_reset/$', views.PasswordResetView.as_view(), name='account_password_reset'),
                       url(r'^signup/$', 'signup', name='signup'),
)
