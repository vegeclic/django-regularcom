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

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.shortcuts import render, redirect, resolve_url
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
import django.contrib.auth as auth
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import login as auth_views_login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib import messages
from common import views as cv
from . import forms, models
import mailbox.models as mm

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
            account = models.Account.objects.create_user(email=signup_form.data['email'])
            messages.success(request, _("Your account has been successfully created."))
            return redirect('login')

        cv.messages_from_form(request, signup_form)
        return render(request, 'registration/login.html', {'section': 'signup', 'signup_form': signup_form})

    return render(request, 'registration/login.html', {'section': 'signup', 'signup_form': forms.AccountCreationForm()})

def login(request):
    response = auth_views_login(request, extra_context={'section': 'login'}, authentication_form=forms.AccountAuthenticationForm)
    if request.method == 'POST':
        if 'context_data' in dir(response):
            form = response.context_data.get('form')
            if form:
                cv.messages_from_form(request, form)
                return response
        messages.success(request, _("You're logged in."))
    return response

def login_link(request, **kwargs):
    email = kwargs.get('email')
    password = kwargs.get('password')

    redirect_to = request.REQUEST.get(auth.REDIRECT_FIELD_NAME, '')

    if request.method == "GET":
        user = auth.authenticate(username=email, password=password)

        if user is not None:
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth.login(request, user)

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            messages.success(request, _("You're logged in."))

            return HttpResponseRedirect(redirect_to)

    messages.error(request, _("Vos identifiants de connexion sont incorrects. Si vous n'êtes pas encore inscrit, nous vous invitons à vous inscrire en cliquant sur « Inscription » dans le cas contraire, cliquez sur le lien « J'ai oublié mon mot de passe »."))
    redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

    return HttpResponseRedirect(redirect_to)

def logout(request):
    auth_logout(request)
    messages.success(request, _("You're logged out."))
    return login(request)

class PasswordResetView(generic.FormView):
    template_name = 'accounts/password_reset.html'
    form_class = forms.PasswordResetForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        email = form.cleaned_data.get('email').lower()

        try:
            account = models.Account.objects.get(email=email)
        except models.Account.DoesNotExist:
            messages.error(self.request, "Cette adresse email n'existe pas dans notre base de données. Assurez-vous qu'il s'agit bien de cette adresse que vous avez utilisé lors de l'inscription. Si le problème persiste contactez nous à l'adresse suivante: %s" % settings.EMAIL_ADMIN)
        else:
            password = models.Account.objects.make_random_password()
            account.set_password(password)
            account.save()
            customer = account.customer

            mm.Message.objects.create_message(mail_only=True, participants=[customer], subject=_('Password reset'), body=_(
"""Hi %(name)s,

A request to reset your password was made with your account %(email)s from the website of Végéclic.

You will find your new password below:

New password: %(password)s

Best regards,
Végéclic.
"""
            ) % {'name': customer.main_address.__unicode__() if customer.main_address else '', 'email': account.email, 'password': password})

            messages.success(self.request, _('The password has been regenerated. You will receive an email with the new password.'))

        return super().form_valid(form)
