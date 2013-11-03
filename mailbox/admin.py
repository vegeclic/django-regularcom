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

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from isoweek import Week
from dateutil.relativedelta import relativedelta
from . import forms, models
import common.admin as ca
import common.models as cm

class ReplyInline(admin.StackedInline):
    model = models.Reply
    extra = 1

class MessageAdmin(ca.MyModelAdmin):
    form = forms.MessageAdmin
    list_display = ('id', 'owner', 'subject', 'body', 'date_created',)
    list_filter = ('owner',)
    search_fields = ('participants__main_address__last_name', 'participants__main_address__first_name', 'participants__account__email', 'owner__main_address__last_name', 'owner__main_address__first_name', 'owner__account__email',)
    ordering = ('-date_created',)
    filter_horizontal = ('participants', 'participants_notified', 'participants_read',)
    inlines = [ReplyInline,]

admin.site.register(models.Message, MessageAdmin)
