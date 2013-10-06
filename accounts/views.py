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
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import login as auth_views_login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib import messages
from common import views as cv
from . import forms, models

class AccountView(generic.DetailView):
    model = models.Account
    template_name = 'accounts/profile.html'

    def get_object(self): return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'profile'
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

def signup(request):
    if request.method == "POST":
        signup_form = forms.AccountCreationForm(request.POST)

        if signup_form.is_valid():
            # account = models.Account.objects.create_user(email=signup_form.data['email'], password=signup_form.data['password1'])
            account = models.Account.objects.create_user(email=signup_form.data['email'])
            messages.success(request, "Your account has been successfully created.")
            return redirect('login')

        cv.messages_from_form(request, signup_form)
        return render(request, 'registration/login.html', {'section': 'signup', 'signup_form': signup_form})

    return render(request, 'registration/login.html', {'section': 'signup', 'signup_form': forms.AccountCreationForm()})

def login(request):
    response = auth_views_login(request, extra_context={'section': 'login'})
    if request.method == 'POST':
        if 'context_data' in dir(response):
            form = response.context_data.get('form')
            if form:
                cv.messages_from_form(request, form)
                return response
        messages.success(request, "You're logged in.")
    return response

def logout(request):
    auth_logout(request)
    messages.success(request, "You're logged out.")
    return login(request)

def password_reset(request): return redirect('regularcom.views.home')
