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

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.core.cache import cache
import carts.models as cm
import blog.views as bv
import blog.models as bm

class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'home'
        context['thematic_list'] = cache.get('thematic_list') or cm.Thematic.objects.filter(enabled=True).select_related('main_image').order_by('name').all()
        if not cache.get('thematic_list'): cache.set('thematic_list', context['thematic_list'])
        bv.set_common_context_data(context)
        last_recipes = bm.Article.objects.filter(tags__tag='recette').order_by('-period_start', '-date_created').all()
        if last_recipes:
            context['last_recipe'] = last_recipes[0]
        cart_exemple = bm.Article.objects.filter(tags__tag='exemple').order_by('-period_start', '-date_created').all()
        if cart_exemple:
            context['cart_exemple'] = cart_exemple[0]
            
        return context

class HowView(generic.TemplateView):
    template_name = 'how.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'how'
        return context

class ChatView(generic.TemplateView):
    template_name = 'chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'chat'
        return context
