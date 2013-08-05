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
