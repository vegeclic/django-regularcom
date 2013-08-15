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
from django.contrib.auth import logout
from .forms import AccountCreationForm
from .models import Account

# Create your views here.

def signup(request):
    if request.method == "POST":
        signup_form = AccountCreationForm(request.POST)
        if signup_form.is_valid():
            account = Account.objects.create_user(email=signup_form.data['email'], password=signup_form.data['password1'])
            return redirect('django.contrib.auth.views.login', {'signup_ok': True})
        return render(request, 'registration/login.html', {'signup_form': signup_form})
    return render(request, 'registration/login.html', {'signup_form': AccountCreationForm()})
