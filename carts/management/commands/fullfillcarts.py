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
import numpy as np, random
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
        max_quantity = 2
        margin = .1
        zero = True
        debug = False

        if debug: logging.debug('DEBUG MODE')

        week_limit = Week.withdate(Week.thisweek().sunday() + relativedelta(days=9))
        deliveries = models.Delivery.objects.filter(date__lte=week_limit, status='p', subscription__enabled=True)
        for delivery in deliveries:
            logging.debug(delivery.__unicode__())

            subscription = delivery.subscription
            subscription_weight = subscription.size.weight - subscription.size.weight*settings.PACKAGING_WEIGHT_RATE/100
            subscription_price = subscription.price().price
            carrier = subscription.carrier
            weight_level = carrier.carrierlevel_set.filter(weight__gte=subscription.size.weight)
            if weight_level:
                logging.debug('weight_level: %s kg (%s €)' % (weight_level[0].weight, weight_level[0].price))
                subscription_price -= weight_level[0].price

            logging.debug('carrier: %s' % carrier.name)
            logging.debug('subscription_weight: %s kg' % subscription_weight)
            logging.debug('subscription_price: %s € (%s €)' % (subscription_price, subscription.price().price))

            for extent in subscription.extent_set.all():
                __extent = extent.extent

                logging.debug('meta-product: %s, extent: %s' % (extent.product.name, __extent))

                if extent.customized:
                    logging.debug("start fullfilling the delivery cart with a custom content")

                    logging.debug("create custom content object")
                    content = delivery.content_set.create(product=extent.product, extent=extent.extent, customized=extent.customized) if not debug else None
                    extent_content = extent.extentcontent_set.get()

                    for ecp in extent_content.extentcontentproduct_set.all():
                        logging.debug("add product %s (%d) with a quantity %d (price: %s, weight: %s)" % (ecp.product.name, ecp.product.id, ecp.quantity, ecp.product.price().__unicode__(), ecp.product.weight))
                        if not debug:
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
                weights = [int(p.weight) for p in products]

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

                from deap import algorithms, base, creator, tools

                pareto = tools.selNSGA2
                # pareto = tools.selSPEA2
                algo = algorithms.eaMuPlusLambda
                # algo = algorithms.eaMuCommaLambda

                creator.create("Fitness", base.Fitness, weights=(-1.0,-1.0,-1.0,-1.0,))
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
                # def mut(individual): return tools.mutation.mutUniformInt(individual, min_quantity, max_quantity, 0.01)

                def cx(ind1, ind2):
                    site = random.randint(0, min(len(ind1), len(ind2)))
                    ind1[:site], ind2[:site] = ind2[:site], ind1[:site]
                    return ind1, ind2

                def mut(individual):
                    pos = random.randint(0, nbr_items-1)
                    individual[pos] = random.randint(min_quantity, max_quantity)
                    return individual,

                toolbox.register("evaluate", eval)
                toolbox.register("mate", cx)
                toolbox.register("mutate", mut)
                toolbox.register("select", pareto)

                pop = toolbox.population(n=pop_size)
                hof = tools.ParetoFront()
                new_pop, logbook = algo(pop, toolbox, pop_size, lambda_algo, cxpb, mutpb, max_gen, halloffame=hof, verbose=0)

                logging.debug("len(hof): %d" % len(hof))
                logging.debug("len(products): %s" % len(products))
                logging.debug("prices (€): %s" % prices)
                logging.debug("weights (g): %s" % weights)
                logging.debug("criterias: %s" % criterias)
                logging.debug("total_price: %f €" % total_price)
                logging.debug("total_weight: %f g" % total_weight)
                logging.debug("total_criteria: %f" % total_criteria)

                margin_hof = []

                for m in np.arange(margin, 1, margin):
                    logging.debug("trial margin hof with %.2f", m)
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

                sol = hof[ sorted[0][0] ]

                logging.debug("sol: %s" % sol)
                logging.debug("sol.fitness: %s" % sol.fitness)

                assert len(sol) == nbr_items

                logging.debug("start fullfilling the delivery cart content")

                logging.debug("create content object")
                content = delivery.content_set.create(product=extent.product, extent=extent.extent, customized=extent.customized) if not debug else None

                for i in range(nbr_items):
                    if sol[i]:
                        logging.debug("add product %s (%d - %d) with a quantity %d (price: %f, weight: %f)" % (products[i].name, i, products[i].id, sol[i], prices[i], weights[i]))
                        if not debug:
                            content.contentproduct_set.create(product=products[i], quantity=sol[i])

            if not debug:
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
                ) % {'name': customer.main_address.__unicode__() if customer.main_address else '', 'date': delivery.get_date_display(), 'subscription_id': subscription.id})

        translation.deactivate()
