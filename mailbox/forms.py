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
from django import forms
from django.utils.translation import ugettext_lazy as _
from . import models
import common.forms as cf
import common.models as cm
import products.models as pm
import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week
from pprint import pprint

class NewMessage(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ('participants', 'subject', 'body',)

    def __init__(self, *args, **kwargs):
        super(NewMessage, self).__init__(*args, **kwargs)
        for field in ['participants', 'subject', 'body',]:
            self.fields.get(field).widget.attrs['class'] = 'input-block-level'
        self.fields.get('body').widget.attrs['rows'] = '10'

class ReplyMessage(forms.ModelForm):
    class Meta:
        model = models.Reply
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super(ReplyMessage, self).__init__(*args, **kwargs)
        for field in ['body',]:
            self.fields.get(field).widget.attrs['class'] = 'input-block-level'
        self.fields.get('body').widget.attrs['rows'] = '10'
