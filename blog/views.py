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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from . import models, forms

def set_common_context_data(context):
    context['categories'] = models.Category.objects.all()
    context['tags'] = models.TaggedItem.objects.distinct('tag').order_by('tag').all()
    context['last_articles'] = models.Article.objects.order_by('-date_last_modified').all()
    context['comments'] = models.Comment.objects.order_by('-date_created').all()

class BlogView(generic.ListView):
    model = models.Article
    template_name = 'blog/blog.html'

    def get_queryset(self):
        articles = models.Article.objects.order_by('-date_created').all()

        paginator = Paginator(articles, 10)

        page = self.kwargs.get('page', 1)
        try:
            articles_per_page = paginator.page(page)
        except PageNotAnInteger:
            articles_per_page = paginator.page(1)
        except EmptyPage:
            articles_per_page = paginator.page(paginator.num_pages)

        return articles_per_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'blog'
        set_common_context_data(context)
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class CategoryView(generic.ListView):
    model = models.Article
    template_name = 'blog/blog.html'

    def get_queryset(self):
        articles = models.Article.objects.order_by('-date_last_modified').filter(categories__id=self.kwargs.get('pk')).all()

        paginator = Paginator(articles, 10)

        page = self.kwargs.get('page', 1)
        try:
            articles_per_page = paginator.page(page)
        except PageNotAnInteger:
            articles_per_page = paginator.page(1)
        except EmptyPage:
            articles_per_page = paginator.page(paginator.num_pages)

        return articles_per_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'blog'
        context['sub_section'] = 'category'
        set_common_context_data(context)
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class TagView(generic.ListView):
    model = models.Article
    template_name = 'blog/blog.html'

    def get_queryset(self):
        articles = models.Article.objects.order_by('-date_last_modified').filter(tags__tag=self.kwargs.get('tag')).all()

        paginator = Paginator(articles, 10)

        page = self.kwargs.get('page', 1)
        try:
            articles_per_page = paginator.page(page)
        except PageNotAnInteger:
            articles_per_page = paginator.page(1)
        except EmptyPage:
            articles_per_page = paginator.page(paginator.num_pages)

        return articles_per_page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'blog'
        context['sub_section'] = 'tag'
        set_common_context_data(context)
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ArticleView(generic.DetailView):
    model = models.Article
    template_name = 'blog/article.html'

    def get_object(self):
        return models.Article.objects.get(id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'blog'
        context['sub_section'] = 'article'
        context['articles'] = models.Article.objects.order_by('?').all()
        set_common_context_data(context)
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class NewCommentView(generic.CreateView):
    form_class = forms.NewComment
    model = models.Comment
    template_name = 'blog/new_comment.html'
    success_url = '/blog/'

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        fi = form.instance
        if self.request.user.is_authenticated():
            fi.participant = self.request.user
        fi.article = models.Article.objects.get(id=pk)
        self.success_url = reverse_lazy('article_slug', args=[pk, fi.article.slug])
        ret = super().form_valid(form)
        messages.success(self.request, _('Your comment has been sent successfuly.'))
        return ret

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'blog'
        context['sub_section'] = 'new_comment'
        context['object'] = models.Article.objects.get(id=self.kwargs.get('pk'))
        set_common_context_data(context)
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
