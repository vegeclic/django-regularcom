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

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.formtools.wizard.views import WizardView, SessionWizardView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.cache import never_cache, cache_control
from customers import models as cm
from . import forms, models
import products.models as pm
from dateutil.relativedelta import relativedelta
from isoweek import Week

class MessageListView(generic.ListView):
    model = models.Message

    def get_queryset(self):
        return models.Message.objects.filter(participants__account=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'mailbox'
        context['sub_section'] = 'messages'
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class MessageView(generic.DetailView):
    model = models.Message

    def get_object(self):
        message = models.Message.objects.get(id=self.kwargs.get('pk'), participants__account=self.request.user)
        customer = cm.Customer.objects.get(account=self.request.user)
        if customer not in message.participants_read.all():
            print(customer)
            message.participants_read.add(customer)
            message.save()
        return message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'mailbox'
        context['sub_section'] = 'messages'
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class NewMessageView(generic.CreateView):
    form_class = forms.NewMessage
    model = models.Message
    template_name = 'mailbox/new_message.html'
    success_url = '/mailbox/messages/'

    def form_valid(self, form):
        fi = form.instance
        fi.owner = cm.Customer.objects.get(account=self.request.user)
        ret = super().form_valid(form)
        fi.participants.add(fi.owner)
        fi.participants_read.add(fi.owner)
        fi.participants_notified.add(fi.owner)
        messages.success(self.request, _('Your message has been sent successfuly.'))
        models.create_mail(subject=fi.subject,
                           body=fi.body,
                           participants=fi.participants.exclude(fi.owner),
                           message=fi)
        return ret

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'mailbox'
        context['sub_section'] = 'new_message'
        context['form'].fields.get('participants').queryset = cm.Customer.objects.exclude(account=self.request.user)
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ReplyMessageView(generic.CreateView):
    form_class = forms.ReplyMessage
    model = models.Reply
    template_name = 'mailbox/reply_message.html'
    success_url = '/mailbox/messages/'

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        fi = form.instance
        fi.participant = cm.Customer.objects.get(account=self.request.user)
        fi.message = models.Message.objects.get(id=pk, participants__account=self.request.user)
        fi.message.participants_read.clear()
        fi.message.participants_notified.clear()
        fi.message.participants_read.add(fi.participant)
        fi.message.participants_notified.add(fi.participant)
        self.success_url = reverse_lazy('message_detail', args=[pk])
        ret = super().form_valid(form)
        messages.success(self.request, _('Your reply has been sent successfuly.'))
        to = list(fi.message.participants.all())
        to.remove(fi.participant)
        models.create_mail(subject=fi.message.subject, body=fi.body, participants=to, owner=fi.participant, message=fi.message, prefix='Re: ')
        return ret

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'mailbox'
        context['sub_section'] = 'messages'
        context['object'] = models.Message.objects.get(id=self.kwargs.get('pk'), participants__account=self.request.user)
        return context

    @method_decorator(login_required)
    @cache_control(private=True)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
