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
from mailbox import models as mm
from customers import models as cm
import logging, logging.config

logging.config.fileConfig('carts/management/commands/logging.conf')

class Command(NoArgsCommand):
    help = 'apply direct debits'

    def handle_noargs(self, **options):
        translation.activate('fr')

        logging.debug('Command in progress')

        debug = False

        if debug: logging.debug('DEBUG MODE')

        week_limit = Week.withdate(Week.thisweek().sunday() + relativedelta(days=9))

        # first changed the status of expired deliveries
        deliveries_canceled = models.Delivery.objects.filter(date__lt=week_limit, status='w', subscription__enabled=True)
        for delivery in deliveries_canceled:
            logging.debug('delivery %d expired' % delivery.id)
            if debug: continue
            delivery.status = 'e'
            delivery.save()

        # secondly, get all the deliveries with a date higher or equal to J+9 and lesser than J+9+7 with a waiting status and a subscription which accepts direct debit.
        deliveries = models.Delivery.objects.filter(date__gte=week_limit, date__lt=week_limit+1, status='w', subscription__direct_debit=True, subscription__enabled=True)

        for delivery in deliveries:
            customer = delivery.subscription.customer
            wallet = customer.wallet
            payed_deliveries = delivery.subscription.delivery_set.filter(status__in=delivery.SUCCESS_CHOICES)
            delivery.payed_price = delivery.subscription.price().price/(1+views.DeliveryView.q/100)**len(payed_deliveries.all())
            delivery.status = 'p'

            try:
                delivery.save()
            except ValueError as e:
                logging.debug('delivery %d not payed' % delivery.id)
                if not debug:
                    message = mm.Message.objects.create_message(participants=[customer], subject=_('Delivery %(date)s cannot be validated') % {'date': delivery.get_date_display()}, body=_(
"""Hi %(name)s,

with some regret I must report that we were unable to validate your delivery %(date)s from the subscription %(subscription_id)d since you dont have enough money in your wallet to buy it.

Please take a moment to credit your wallet first and validate the delivery back.

Best regards,
Végéclic.
"""
                    ) % {'name': customer.main_address.__unicode__() if customer.main_address else '', 'date': delivery.get_date_display(), 'subscription_id': delivery.subscription.id})
            else:
                logging.debug('delivery %d payed' % delivery.id)
                if not debug:
                    message = mm.Message.objects.create_message(participants=[customer], subject=_('Delivery %(date)s has been validated') % {'date': delivery.get_date_display()}, body=_(
"""Hi %(name)s,

we are pleased to announce your delivery %(date)s from the subscription %(subscription_id)d has been validated automatically.

Your cart will be prepared as soon as possible and send to you in 10-12 days.

Best regards,
Végéclic.
"""
                    ) % {'name': customer.main_address.__unicode__() if customer.main_address else '', 'date': delivery.get_date_display(), 'subscription_id': delivery.subscription.id})

        translation.deactivate()
