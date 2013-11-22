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
from ... import models

logging.config.fileConfig('carts/management/commands/logging.conf')

class Command(NoArgsCommand):
    help = 'Generate a list of order of suppliers products'

    def handle_noargs(self, **options):
        translation.activate('fr')

        week_limit = Week.withdate(Week.thisweek().day(settings.VALIDATING_DAY_OF_WEEK) + relativedelta(days=settings.DELAY_BETWEEN_DEFINITON_N_DELIVERY))
        deliveries = models.Delivery.objects.filter(date__lte=week_limit, status='P', subscription__enabled=True).order_by('subscription__customer__account__email')

        for delivery in deliveries:
            logger_delivery = logging.getLogger('[delivery %d]' % delivery.id)

            subscription = delivery.subscription
            customer = subscription.customer

            logger_delivery.info(delivery.__unicode__())

            for extent in subscription.extent_set.all():
                __extent = extent.extent

                logger_extent = logging.getLogger('[delivery %d] [%s] [%s%%]' % (delivery.id, extent.product.name, __extent))


                logger_extent.debug('meta-product: %s, extent: %s' % (extent.product.name, __extent))
                logger_extent = logging.getLogger('[delivery %d] [%s] [%s%%] [custom]' % (delivery.id, extent.product.name, __extent))


        translation.deactivate()
