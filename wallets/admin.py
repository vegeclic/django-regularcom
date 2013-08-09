from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from . import models
import common.admin as ca
import common.models as cm

class WalletAdmin(ca.MyModelAdmin):
    list_display = ('customer', 'balance', 'currency',)

admin.site.register(models.Wallet, WalletAdmin)
