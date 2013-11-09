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
                       url(r'^$', views.BlogView.as_view(), name='blog'),
                       url(r'^article/(?P<pk>\d+)/$', views.ArticleView.as_view(), name='article'),
                       url(r'^category/(?P<pk>\d+)/$', views.CategoryView.as_view(), name='category'),
                       url(r'^tag/(?P<tag>\w+)/$', views.TagView.as_view(), name='tag'),
                       url(r'^new_comment/(?P<pk>\d+)/$', views.NewCommentView.as_view(), name='new_comment'),
)
