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
import twitter

logging.config.fileConfig(settings.BASE_DIR + '/blog/management/commands/logging.conf')

class Command(NoArgsCommand):
    help = 'Send an article to twitter'

    option_list = BaseCommand.option_list + (
        make_option('-t', '--test', action='store_true', dest='test', default=False, help='Test mode (no changes applied) [default: %default]'),
    )

    def handle_noargs(self, **options):
        translation.activate('fr')
        today, now = datetime.date.today(), datetime.datetime.now()

        for message in models.Microblog.objects.filter(date_last_sent=None).all():
            message.date_last_sent = now
            message.save()

        qs = models.Microblog.objects.filter(article__enabled=True, article__period_start__lte=today, article__period_end__gte=today).order_by('date_last_sent', 'article__date_created')

        if not qs.exists():
            logging.debug('No more messages available for sending')
            return

        message = qs.all()[0]

        link = 'http://www.vegeclic.fr%s' % reverse_lazy('article_slug', args=[message.article.id, message.article.slug])
        body = '%s #Vegeclic #Vegan %s' % (message.message[:110], link)

        logging.info('Sending message "%s"' % body)

        for tk in settings.TWITTER_ACCOUNTS:
            t = twitter.Twitter(auth=twitter.OAuth(tk['oauth_token'], tk['oauth_secret'],
                                                   tk['consumer_key'], tk['consumer_secret']))

            logging.info('… to %s' % tk['oauth_token'])

            if not options['test']: t.statuses.update(status=body)

        if not options['test']:
            message.date_last_sent = now
            message.save()

        translation.deactivate()
