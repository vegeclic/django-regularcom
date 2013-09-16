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

from django.http import HttpResponse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from . import models
import customers.models as cm

class MailboxMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated(): return None
        msgs = models.Message.objects.filter(participants__account=request.user)
        customer = cm.Customer.objects.get(account=request.user)
        for msg in msgs:
            if customer not in msg.participants_notified.all():
                messages.success(request, _('You have received a new message: %s (see Mailbox).') % msg.subject)
                msg.participants_notified.add(customer)
                msg.save()
        return None

    def process_template_response(self, request, response):
        if not request.user.is_authenticated(): return response
        msgs = models.Message.objects.filter(participants__account=request.user).exclude(participants_read__account=request.user)
        if len(msgs): response.context_data['nb_messages'] = len(msgs)
        return response