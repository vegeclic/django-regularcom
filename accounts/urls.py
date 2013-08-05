from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^profile/$', 'regularcom.views.home', name='home'),
    url(r'^password_reset/$', 'regularcom.views.home', name='home'),
    url(r'^signup/$', 'accounts.views.signup'),
)
