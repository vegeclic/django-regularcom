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
from optparse import make_option
import datetime
from dateutil.relativedelta import relativedelta
from isoweek import Week
from ... import models
from mailbox import models as mm
from customers import models as cm
import logging, logging.config
import numpy as np, random
import matplotlib.pyplot as plt
import readline
from deap import algorithms, base, creator, tools

logging.config.fileConfig('carts/management/commands/logging.conf')

class Command(NoArgsCommand):
    help = 'Interactive version of fullfilling algorithm to validate subscription deliveries content'

    option_list = BaseCommand.option_list + (
        make_option('-t', '--test', action='store_true', dest='test', default=False, help='test mode (no changes applied) [default: %default]'),
        make_option('--pop_size', action='store', type='int', dest='pop_size', default=50, help='population size [default: %default]'),
        make_option('--max_gen', action='store', type='int', dest='max_gen', default=50, help='maximum number of generations [default: %default]'),
        make_option('--lambda_algo', action='store', type='int', dest='lambda_algo', default=100, help='lambda parameter of algorithm [default: %default]'),
        make_option('--cxpb', action='store', type='float', dest='cxpb', default=.7, help='xover probability [default: %default]'),
        make_option('--mutpb', action='store', type='float', dest='mutpb', default=.2, help='mutation probability [default: %default]'),
        make_option('--min_quantity', action='store', type='int', dest='min_quantity', default=0, help='minimum quantity [default: %default]'),
        make_option('--max_quantity', action='store', type='int', dest='max_quantity', default=2, help='maximum quantity [default: %default]'),
        make_option('--margin', action='store', type='float', dest='margin', default=.1, help='initial margin price extent value [default: %default]'),
        make_option('--zero_init', action='store_true', dest='zero', default=True, help='solution initialized to zero values [default: %default]'),
        make_option('--random_init', action='store_false', dest='zero', help='solution initialized to random values'),
        make_option('--NSGA2', action='store_true', dest='pareto', help='NSGAII selection pareto stategy [default: %default]'),
        make_option('--SPEA2', action='store_false', dest='pareto', help='SPEAII selection pareto stategy'),
        make_option('--plus', action='store_true', dest='algo', help='Plus EA algorithm stategy [default: %default]'),
        make_option('--comma', action='store_false', dest='algo', help='Comma EA algorithm stategy'),
    )

    @staticmethod
    def print_interactive_usage():
        logging.info('*' * 50)
        logging.info(' ' * 15 + 'Interactive usage')
        logging.info('*' * 50)
        logging.info('* [CTRL+C] to stop program')
        logging.info('* [CTRL+D] to stop program')
        logging.info('*' * 50)
        logging.info('')

    def handle_noargs(self, **options):
        translation.activate('fr')
        logging.debug('Command in progress')

        self.print_interactive_usage()

        if options['test']:
            logging.info('[TEST MODE enabled]')
            logging.info('')

        week_limit = Week.withdate(Week.thisweek().day(settings.VALIDATING_DAY_OF_WEEK) + relativedelta(days=9))
        deliveries = models.Delivery.objects.filter(date__lte=week_limit, status='p', subscription__enabled=True)

        logging.info('Number of deliveries to fullfill: %d' % deliveries.count())

        for delivery in deliveries:
            logger_delivery = logging.getLogger('[delivery %d]' % delivery.id)

            logger_delivery.info('')
            logger_delivery.info('Process the delivery: %s' % delivery.__unicode__())
            logger_delivery.info('')

            subscription = delivery.subscription
            subscription_weight = subscription.size.weight - subscription.size.weight*settings.PACKAGING_WEIGHT_RATE/100
            subscription_price = subscription.price().price
            carrier = subscription.carrier
            weight_level = carrier.carrierlevel_set.filter(weight__gte=subscription.size.weight)
            if weight_level:
                logger_delivery.info('weight level:\t\t%s kg (%s €)' % (weight_level[0].weight, weight_level[0].price))
                subscription_price -= weight_level[0].price

            logger_delivery.info('carrier:\t\t%s' % carrier.name)
            logger_delivery.info('subscription weight:\t%s kg' % subscription_weight)
            logger_delivery.info('subscription price:\t%s € (%s €)' % (subscription_price, subscription.price().price))
            logger_delivery.info('')

            for extent in subscription.extent_set.all():
                __extent = extent.extent

                logger_extent = logging.getLogger('[delivery %d] [%s] [%s%%]' % (delivery.id, extent.product.name, __extent))


                logger_extent.debug('meta-product: %s, extent: %s' % (extent.product.name, __extent))

                if extent.customized:
                    logger_extent = logging.getLogger('[delivery %d] [%s] [%s%%] [custom]' % (delivery.id, extent.product.name, __extent))

                    logger_extent.info('start fullfilling the delivery cart with a custom content')

                    logger_extent.info('create custom content object')
                    content = delivery.content_set.create(product=extent.product, extent=extent.extent, customized=extent.customized) if not options['test'] else None
                    extent_content = extent.extentcontent_set.get()

                    for ecp in extent_content.extentcontentproduct_set.all():
                        logger_extent.info('+ %d x %30s\t\t(%d,\t%s€,\t%sg)' % (ecp.quantity, ecp.product.name[:30], ecp.product.id, ecp.product.price().__unicode__(), ecp.product.weight))
                        if not options['test']:
                            content.contentproduct_set.create(product=ecp.product, quantity=ecp.quantity)

                    continue

                def get_product_products(product):
                    __products = []
                    for child in product.products_children.all():
                        __products += get_product_products(child)
                    __products += product.product_product.filter(status='p').all()
                    return __products

                products = get_product_products(extent.product)
                nbr_items = len(products)

                prices = [p.main_price.get_after_tax_price_with_fee() if carrier.apply_suppliers_fee else p.main_price.get_after_tax_price() for p in products]
                weights = [int(p.weight or settings.DEFAULT_WEIGHT) for p in products]

                criterias = []
                if subscription.criterias.all():
                    for p in products:
                        __filter = p.criterias
                        for c in subscription.criterias.filter(enabled=True).all():
                            __filter = __filter.filter(id=c.id)
                        criterias.append(len(__filter.all()))
                else:
                    criterias = [0] * nbr_items

                total_price = round(subscription_price*__extent/100, 2)
                total_weight = round(subscription_weight*__extent/100*1000, 2)
                total_criteria = round(sum(criterias), 2)

                creator.create("Fitness", base.Fitness, weights=(-1.0,-1.0,-1.0,-1.0,))
                creator.create("Individual", list, fitness=creator.Fitness)

                toolbox = base.Toolbox()

                if options['zero']:
                    toolbox.register("quantity_item", lambda: options['min_quantity'])
                else:
                    toolbox.register("quantity_item", random.randint, options['min_quantity'], options['max_quantity'])

                toolbox.register("individual", tools.initRepeat, creator.Individual,
                                 toolbox.quantity_item, nbr_items)
                toolbox.register("population", tools.initRepeat, list, toolbox.individual)

                def eval(individual):
                    eval_total_price = 0.0
                    eval_total_weight = 0.0
                    eval_total_criteria = 0.0
                    for i in range(nbr_items):
                        eval_total_price += individual[i] * prices[i]
                        eval_total_weight += individual[i] * weights[i]
                        eval_total_criteria += individual[i] * criterias[i]
                    return \
                        abs(total_price - eval_total_price),\
                        abs(total_criteria - eval_total_criteria),\
                        plt.mlab.entropy(individual, 1),\
                        abs(total_weight - eval_total_weight),\

                # def cx(ind1, ind2): return tools.crossover.cxOnePoint(ind1, ind2)
                # def mut(individual): return tools.mutation.mutUniformInt(individual, options['min_quantity'], options['max_quantity'], 0.01)

                def cx(ind1, ind2):
                    site = random.randint(0, min(len(ind1), len(ind2)))
                    ind1[:site], ind2[:site] = ind2[:site], ind1[:site]
                    return ind1, ind2

                def mut(individual):
                    pos = random.randint(0, nbr_items-1)
                    individual[pos] = random.randint(options['min_quantity'], options['max_quantity'])
                    return individual,

                pareto = tools.selNSGA2 if options['pareto'] else tools.selSPEA2
                algo = algorithms.eaMuPlusLambda if options['algo'] else algorithms.eaMuCommaLambda

                toolbox.register("evaluate", eval)
                toolbox.register("mate", cx)
                toolbox.register("mutate", mut)
                toolbox.register("select", pareto)

                pop = toolbox.population(n=options['pop_size'])
                hof = tools.ParetoFront()
                new_pop, logbook = algo(pop, toolbox, options['pop_size'], options['lambda_algo'], options['cxpb'], options['mutpb'], options['max_gen'], halloffame=hof, verbose=0)

                logger_extent.debug("len(hof): %d" % len(hof))
                logger_extent.debug("len(products): %s" % len(products))
                logger_extent.debug("prices (€): %s" % prices)
                logger_extent.debug("weights (g): %s" % weights)
                logger_extent.debug("criterias: %s" % criterias)
                logger_extent.debug("total_price: %f €" % total_price)
                logger_extent.debug("total_weight: %f g" % total_weight)
                logger_extent.debug("total_criteria: %f" % total_criteria)

                margin_hof = []

                for m in np.arange(options['margin'], 1, options['margin']):
                    logger_extent.debug("trial margin hof with %.2f", m)
                    trial_margin_hof = []
                    for x in hof:
                        if x.fitness.values[0] <= (total_price*m): trial_margin_hof.append(x)
                    if len(trial_margin_hof) > 0:
                        margin_hof = trial_margin_hof
                        break

                assert len(margin_hof) > 0

                sorted = np.sort(np.array([(i,) + x.fitness.values for i, x in enumerate(margin_hof)],
                                          dtype=[('i', int), ('price', float), ('criterias', float),
                                                 ('diversity', float), ('weight', float)]),
                                          order=['criterias', 'diversity', 'weight', 'price'])

                logger_extent.info('there are %d solutions' % len(sorted))

                for i, fitnesses in enumerate(sorted):
                    logger_solution = logging.getLogger('[delivery %d] [%s] [%s%%] [%d]' % (delivery.id, extent.product.name, __extent, i))

                    sol = hof[ fitnesses[0] ]

                    logger_solution.info('')
                    logger_solution.debug('sol: %s' % sol)
                    logger_solution.info('sol.fitness: %s' % sol.fitness)

                    assert len(sol) == nbr_items

                    for i in range(nbr_items):
                        if sol[i]:
                            logger_solution.info('+ %d x %30s\t(%d,\t%s€,\t%sg)' % (sol[i], products[i].name[:30], products[i].id, prices[i], weights[i]))

                idx = 0
                higherbound = len(sorted)-1
                while True:
                    try:
                        idx = int(input('[Select one solution between 0 and %d]$ ' % higherbound))
                    except TypeError:
                        logger_extent.error('Bad type value passed (a value between 0 and %d)' % higherbound)
                    except ValueError:
                        logger_extent.error('Bad value passed (a value between 0 and %d)' % higherbound)
                    else:
                        if 0 < idx < higherbound+1: break

                logger_extent.info('Start fullfilling the delivery cart content with the solution %d' % idx)

                sol = hof[ sorted[idx][0] ]

                logger_extent.info('Create content object')
                content = delivery.content_set.create(product=extent.product, extent=extent.extent, customized=extent.customized) if not options['test'] else None

                for i in range(nbr_items):
                    if sol[i]:
                        logger_extent.info('+ %d x %30s\t(%d,\t%s€,\t%sg)' % (sol[i], products[i].name[:30], products[i].id, prices[i], weights[i]))
                        if not options['test']:
                            content.contentproduct_set.create(product=products[i], quantity=sol[i])

            if not options['test']:
                logger_extent.info("change delivery status")

                delivery.status = 'P'
                delivery.save()

                logger_extent.info("send a message to the delivery customer")

                customer = subscription.customer

                message = mm.Message.objects.create_message(participants=[customer], subject=_('Delivery %(date)s is in progress') % {'date': delivery.get_date_display()}, body=_(
"""Hi %(name)s,

we are pleased to announce your delivery %(date)s content from the subscription %(subscription_id)d has been defined and will be prepared as soon as possible for sending.

Your cart will be send to you in 10 days.

Best regards,
Végéclic.
"""
                ) % {'name': customer.main_address.__unicode__() if customer.main_address else '', 'date': delivery.get_date_display(), 'subscription_id': subscription.id})

        translation.deactivate()
