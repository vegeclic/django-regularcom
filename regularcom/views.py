from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
# from models import *

def home(request):
    return render(request, 'home.html')
