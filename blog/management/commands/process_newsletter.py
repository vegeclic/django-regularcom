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
from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
import logging, logging.config
from isoweek import Week
from dateutil.relativedelta import relativedelta
import datetime
from django.core.mail import send_mass_mail
from optparse import make_option
from ... import models
import accounts.models as am

logging.config.fileConfig('carts/management/commands/logging.conf')

class Command(NoArgsCommand):
    help = 'Generate a list of order of suppliers products'

    option_list = BaseCommand.option_list + (
        make_option('-b', '--browse', action='store_true', dest='browse', default=False, help='Open product url in browser [default: %default]'),
        make_option('-p', '--pages', action='store', type='int', dest='pages', default=5, help='Choose number of pages to browse step by step [default: %default]'),
    )

    def handle_noargs(self, **options):
        translation.activate('fr')
        today = datetime.date.today()

        for account in am.Account.objects.exclude(newsletter='n').all():
            reader, created = models.Reader.objects.get_or_create(account=account)
            logger_account = logging.getLogger('[%25s]' % account.email[:25])

            qs = models.Article.objects.filter(period_start__gte=today, period_end__lte=today).order_by('date_created')
            if reader.articles_read.exists(): qs = qs.exclude(reader.articles_read.all())
            # logger_article = logging.getLogger('[%25s] [%25s] [%s]' % (account.email[:25], article.title[:25].title(), article.date_created.strftime('%y-%m-%d')))

            if not qs.exists():
                logger_account.info('No more articles available for sending')
                continue

            article = qs.all()[0]

            logger_account.info('Sending article "%25s" (%s)' % (article.title[:25].title(), article.date_created.strftime('%y-%m-%d')))

        translation.deactivate()
