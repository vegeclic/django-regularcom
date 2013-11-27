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
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
import logging, logging.config
from isoweek import Week
from dateutil.relativedelta import relativedelta
import datetime
from django.core import mail
from django.utils.html import strip_tags
from optparse import make_option
import smtplib
from ... import models
import accounts.models as am
import fandjango.models as fm

logging.config.fileConfig(settings.BASE_DIR + '/blog/management/commands/logging.conf')

class Command(NoArgsCommand):
    help = 'Send an article to facebook'

    option_list = BaseCommand.option_list + (
        make_option('-t', '--test', action='store_true', dest='test', default=False, help='Test mode (no changes applied) [default: %default]'),
    )

    def get_graph_api(self, **options):
        oa = fm.OAuthToken.objects.get(user__facebook_id=settings.FACEBOOK_ADMIN_ID)
        logging.debug('oa.token: %s' % oa.token)

        g = fm.GraphAPI(oa.token)
        data = g.get('me/accounts')
        data = data.get('data') or {}
        logging.debug('data: %s' % data)

        page_token = None
        for d in data:
            id = d.get('id', None)
            if id == settings.FACEBOOK_PAGE_ID:
                page_token = d.get('access_token', None)
                break

        logging.debug('page_token: %s' % page_token)

        return [g, fm.GraphAPI(page_token)]

    def handle_noargs(self, **options):
        translation.activate('fr')
        today = datetime.date.today()
        now = datetime.datetime.now()

        gs = self.get_graph_api(**options)
        logging.debug('me: %s' % gs[0].get('me'))

        qs = models.Article.objects.filter(date_last_blogging_sent=None)
        for article in qs.all():
            article.date_last_blogging_sent = now
            article.save()

        qs = models.Article.objects.filter(period_start__lte=today, period_end__gte=today).order_by('date_last_blogging_sent', 'date_created')

        if not qs.exists():
            logging.debug('No more articles available for sending')
            return

        article = qs.all()[0]

        subject = article.title.title()
        body = "%s\n\nPlus de détails à l'adresse : http://www.vegeclic.fr%s\n" % (strip_tags(article.body), reverse_lazy('article_slug', args=[article.id, article.slug]))
        message = '%s\n\n%s' % (subject, body)

        if not options['test']:
            for g in gs:
                if article.main_image:
                    g.post(message=message, path='me/photos', source=open(article.main_image.image.path, 'rb'))
                else:
                    g.post(message=message, path='me/feed')
            article.date_last_blogging_sent = now
            article.save()

        logging.info('Sending article "%25s" (%s)' % (subject[:25], article.date_created.strftime('%y-%m-%d')))

        translation.deactivate()
