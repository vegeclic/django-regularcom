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

# class NewArticleAdmin(forms.ModelForm):
#     class Meta:
#         model = models.Article

#     def save(self, commit=True):
#         article = super().save(commit=False)
#         message.save()
#         models.create_mail(subject=message.subject,
#                            body=message.body,
#                            participants=message.participants.exclude(message.owner),
#                            message=message)
#         return message

# class ArticleAdmin(forms.ModelForm):
#     class Meta:
#         model = models.Article

class NewComment(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['body',]:
            self.fields.get(field).widget.attrs['class'] = 'form-control'
        self.fields.get('body').widget.attrs['rows'] = '10'
