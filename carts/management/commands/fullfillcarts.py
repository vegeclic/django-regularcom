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
from ... import models
from mailbox import models as mm
from customers import models as cm
import logging, logging.config
import numpy, random
import matplotlib.pyplot as plt

logging.config.fileConfig('carts/management/commands/logging.conf')

class Command(NoArgsCommand):
    help = 'Fullfill the validated subscription deliveries content'

    def handle_noargs(self, **options):
        translation.activate('fr')

        logging.debug('Command in progress')

        pop_size = 50
        max_gen = 50
        lambda_algo = 100
        cxpb = .7
        mutpb = .2
        min_quantity = 0
        max_quantity = 10
        marging = .1
        # marging = 0
        zero = True
        # zero = False

        # week_limit = Week.withdate(datetime.date.today() + relativedelta(days=10))
        week_limit = Week.withdate(Week.thisweek().sunday() + relativedelta(days=9))
        deliveries = models.Delivery.objects.filter(date__lte=week_limit, status='p')
        for delivery in deliveries:
            logging.debug(delivery.__unicode__())

            subscription = delivery.subscription
            carrier = subscription.carrier

            for extent in subscription.extent_set.all():
                logging.debug(extent)

                __extent = extent.extent

                def get_product_products(product):
                    __products = []
                    for child in product.products_children.all():
                        __products += get_product_products(child)
                    # __products += product.product_product.all()
                    __filter = product.product_product
                    for c in subscription.criterias.all(): __filter = __filter.filter(criterias=c)
                    __products += __filter.all()
                    return __products

                products = get_product_products(extent.product)
                prices = [p.price().get_after_tax_price_with_fee() if carrier.apply_suppliers_fee else p.price().get_after_tax_price() for p in products]
                weights = [p.weight for p in products]
                nbr_items = len(products)

                total_price = subscription.price().price*__extent/100
                total_weight = subscription.size.weight*__extent/100

                from deap import algorithms, base, creator, tools

                pareto = tools.selNSGA2
                # pareto = tools.selSPEA2
                algo = algorithms.eaMuPlusLambda
                # algo = algorithms.eaMuCommaLambda

                creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0))
                creator.create("Individual", list, fitness=creator.Fitness)

                toolbox = base.Toolbox()

                if zero:
                    toolbox.register("quantity_item", lambda: min_quantity)
                else:
                    toolbox.register("quantity_item", random.randint, min_quantity, max_quantity)

                toolbox.register("individual", tools.initRepeat, creator.Individual,
                                 toolbox.quantity_item, nbr_items)
                toolbox.register("population", tools.initRepeat, list, toolbox.individual)

                def eval(individual):
                    eval_total_price = 0.0
                    eval_total_weight = 0.0
                    for i in range(nbr_items):
                        eval_total_price += individual[i] * prices[i]
                        eval_total_weight += individual[i] * (weights[i]/1000)
                    return \
                        abs(total_price - eval_total_price),\
                        abs(total_weight - eval_total_weight),\
                        plt.mlab.entropy(individual, 1),\
                        individual.count(min_quantity),\

                def cx(ind1, ind2): return tools.crossover.cxOnePoint(ind1, ind2)
                def mut(individual): return tools.mutation.mutUniformInt(individual, min_quantity, max_quantity, mutpb)

                toolbox.register("evaluate", eval)
                toolbox.register("mate", cx)
                toolbox.register("mutate", mut)
                toolbox.register("select", pareto)

                pop = toolbox.population(n=pop_size)
                hof = tools.ParetoFront()
                new_pop, logbook = algo(pop, toolbox, pop_size, lambda_algo, cxpb, mutpb, max_gen, halloffame=hof, verbose=0)

                logging.debug("len(hof): %d" % len(hof))
                logging.debug("products len: %s" % len(products))
                logging.debug("prices: %s" % prices)
                logging.debug("weights: %s" % weights)
                logging.debug("total_price: %f" % total_price)
                logging.debug("total_price: %f" % total_weight)
                logging.debug("hof[0]: %s" % hof[0])
                logging.debug("hof[0].fitness: %s" % hof[0].fitness)

                logging.debug("create content object")

                content = delivery.content_set.create(extent=extent)
                sol = hof[0]

                assert len(sol) == nbr_items

                logging.debug("start fullfilling the delivery cart content")

                for i in range(nbr_items):
                    if sol[i]:
                        logging.debug("add product %d with a quantity %d" % (i, sol[i]))
                        content.contentproduct_set.create(product=products[i], quantity=sol[i])

            logging.debug("change delivery status")

            delivery.status = 'P'
            delivery.save()

            logging.debug("send a message to the delivery customer")

            customer = subscription.customer

            message = mm.Message.objects.create_message(participants=[customer], subject=_('Delivery %(date)s is in progress') % {'date': delivery.get_date_display()}, body=_(
"""Hi %(name)s,

we are pleased to announce your delivery %(date)s content from the subscription %(subscription_id)d has been defined and will be prepared as soon as possible for sending.

Your cart will be send to you in 10 days.

Best regards,
Végéclic.
"""
            ) % {'name': customer.main_address.__unicode__(), 'date': delivery.get_date_display(), 'subscription_id': subscription.id})

        translation.deactivate()
