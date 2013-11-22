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
import webbrowser
from optparse import make_option
from ... import models
import sys

logging.config.fileConfig('carts/management/commands/logging.conf')

class Command(NoArgsCommand):
    help = 'Generate a list of order of suppliers products'
    
    option_list = BaseCommand.option_list + (
        make_option('-b', '--browse', action='store_true', dest='browse', default=False, help='Open product url in browser [default: %default]'),
        make_option('-p', '--pages', action='store', type='int', dest='pages', default=5, help='Choose number of pages to browse step by step [default: %default]'),
    )

    def handle_noargs(self, **options):
        translation.activate('fr')

        week_limit = Week.withdate(Week.thisweek().day(settings.VALIDATING_DAY_OF_WEEK) + relativedelta(days=settings.DELAY_BETWEEN_DEFINITON_N_DELIVERY))
        deliveries = models.Delivery.objects.filter(date__lte=week_limit, status='P', subscription__enabled=True).order_by('subscription__customer__account__email')
        count=0

        for delivery in deliveries:
            logger_delivery = logging.getLogger('[%d]' % delivery.id)

            subscription = delivery.subscription
            customer = subscription.customer

            logger_delivery.info(delivery.__unicode__())

            for content in delivery.content_set.all():
                __extent = content.extent

                logger_content = logging.getLogger('[%d] [%20s%c] [%3s%%]' % (delivery.id, content.product.name[:20], '*' if content.customized else ' ', __extent))
                
                for contentproduct in content.contentproduct_set.all():
                        logger_content.info('%d x %20s (%4d) %s' % (contentproduct.quantity, contentproduct.product.name[:20], contentproduct.product.id, contentproduct.product.main_price.supplier_product_url))
                        if options['browse']:
                                webbrowser.open(contentproduct.product.main_price.supplier_product_url)
                                count += 1
                                if count >= options['pages']: 
                                        count = 0
                                        try: input()
                                        except KeyboardInterrupt: print('Interrupted'); sys.exit()
                        
            logger_delivery.info('')
                        


        translation.deactivate()
