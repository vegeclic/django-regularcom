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
from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week
from ... import models
import logging, logging.config
import numpy, random
import matplotlib.pyplot as plt

logging.config.fileConfig('carts/management/commands/logging.conf')

class Command(NoArgsCommand):
    help = 'Fullfill the validated subscription deliveries content'

    def handle_noargs(self, **options):
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

        week_limit = Week.withdate(datetime.date.today() + relativedelta(days=10))
        deliveries = models.Delivery.objects.filter(date__lte=week_limit, status='p')
        for delivery in deliveries:
            logging.debug(delivery.__unicode__())

            for extent in delivery.subscription.extent_set.all():
                __extent = extent.extent
                products = extent.product.product_product.all()
                prices = [p.price().purchase_price for p in products]
                nbr_items = len(prices)

                total_price = delivery.subscription.price().price*__extent/100

                from deap import algorithms, base, creator, tools

                pareto = tools.selNSGA2
                # pareto = tools.selSPEA2
                algo = algorithms.eaMuPlusLambda
                # algo = algorithms.eaMuCommaLambda

                creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0, -1.0))
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
                    for i in range(nbr_items):
                        eval_total_price += individual[i] * prices[i]
                    return \
                        abs(total_price - eval_total_price),\
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
                logging.debug("prices: %s" % prices)
                logging.debug("total_price: %f" % total_price)
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
