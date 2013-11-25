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
import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week
from ... import models, views
import mailbox.models as mm
import customers.models as cm
import logging, logging.config

logging.config.fileConfig(settings.BASE_DIR + '/carts/management/commands/logging.conf')

class Command(NoArgsCommand):
    help = 'apply direct debits'

    def handle_noargs(self, **options):
        translation.activate('fr')

        logging.debug('Command in progress')

        week_limit = Week.withdate(Week.thisweek().day(settings.VALIDATING_DAY_OF_WEEK) + relativedelta(days=settings.DELAY_BETWEEN_DEFINITON_N_DELIVERY))

        # first changed the status of expired deliveries
        deliveries_canceled = models.Delivery.objects.filter(date__lt=week_limit, status='w', subscription__enabled=True)
        for delivery in deliveries_canceled:
            delivery.status = 'e'
            delivery.save()
            logging.debug('delivery %d expired' % delivery.id)

        # secondly, get all the deliveries with a date higher or equal to J+9 and lesser than J+9+7 with a waiting status and a subscription which accepts direct debit.
        deliveries = models.Delivery.objects.filter(date__gte=week_limit, date__lt=week_limit+1, status='w', subscription__direct_debit=True, subscription__enabled=True)

        for delivery in deliveries:
            delivery.status = 'p'
            try:
                delivery.save()
            except ValueError as e:
                logging.debug('delivery %d not payed' % delivery.id)
            else:
                logging.debug('delivery %d payed' % delivery.id)

        translation.deactivate()
