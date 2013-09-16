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
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms.models import inlineformset_factory
# from django.contrib import messages
import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week
import common.models as cm
import wallets.models as wm

class Message(models.Model):
    owner = models.ForeignKey('customers.Customer', verbose_name=_('owner'))
    participants = models.ManyToManyField('customers.Customer', related_name='mailbox_message_participants', verbose_name=_('participants'))
    subject = models.CharField(_('subject'), max_length=200)
    body = models.TextField(_('body'), blank=True)
    participants_notified = models.ManyToManyField('customers.Customer', null=True, blank=True, related_name='mailbox_message_participants_notified', verbose_name=_('participants_notified'))
    participants_read = models.ManyToManyField('customers.Customer', null=True, blank=True, related_name='mailbox_message_participants_read', verbose_name=_('participants_read'))
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return self.subject

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)
        self.participants_read.add(self.owner)
        self.participants_notified.add(self.owner)

class Reply(models.Model):
    class Meta:
        verbose_name_plural = _('replies')

    message = models.ForeignKey(Message, verbose_name=_('message'))
    participant = models.ForeignKey('customers.Customer', verbose_name=_('participant'))
    body = models.TextField(_('body'), blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self): return self.body
