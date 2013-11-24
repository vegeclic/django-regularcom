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
from ... import models
import accounts.models as am

logging.config.fileConfig('carts/management/commands/logging.conf')

class Command(NoArgsCommand):
    help = 'Generate a list of order of suppliers products'

    option_list = BaseCommand.option_list + (
        make_option('-t', '--test', action='store_true', dest='test', default=False, help='Test mode (no changes applied) [default: %default]'),
    )

    def handle_noargs(self, **options):
        translation.activate('fr')
        today = datetime.date.today()
        connection = mail.get_connection()
        connection.open()

        for account in am.Account.objects.filter(newsletter='i').all():
            reader, created = models.Reader.objects.get_or_create(account=account)
            logger_account = logging.getLogger('[%25s]' % account.email[:25])

            qs = models.Article.objects.filter(period_start__lte=today, period_end__gte=today).order_by('date_created')
            if reader.articles_read.exists(): qs = qs.exclude(id__in=[a.id for a in reader.articles_read.all()])

            if not qs.exists():
                logger_account.debug('No more articles available for sending')
                continue

            article = qs.all()[0]

            subject = '%s%s' % (settings.EMAIL_SUBJECT_PREFIX, article.title.title())
            body = "%s\n\nPlus de détails à l'adresse : http://www.vegeclic.fr%s\n" % (strip_tags(article.body), reverse_lazy('article_slug', args=[article.id, article.slug]))

            if not options['test']:
                email = mail.EmailMessage(subject, body, settings.EMAIL_ADMIN, [account.email], connection=connection)
                if article.main_image:
                    email.attach_file(article.main_image.image.path)
                try:
                    email.send()
                except SMTPSenderRefused:
                    logger_account.error('SMTPSenderRefused')
                    break
                else:
                    reader.articles_read.add(article)

            logger_account.info('Sending article "%25s" (%s)' % (article.title[:25].title(), article.date_created.strftime('%y-%m-%d')))

        connection.close()
        translation.deactivate()
