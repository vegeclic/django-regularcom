#!/usr/bin/env python3

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

import random
import numpy
from pprint import pprint

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

import argparse, logging, sys

import matplotlib.pyplot as plt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The python version of the Dynamic Islands Model for OneMax problem.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--seed', '-s', help='set the seed value for the generator of pseudo-random numbers', type=int, default=0)
    parser.add_argument('--pop_size', '-P', help='size of population', type=int, default=50)
    parser.add_argument('--max_gen', '-G', help='max generation (0: disabled)', type=int, default=50)
    parser.add_argument('--target_fitness', '-T', help='target fitness (0: disabled)', type=int, default=0)
    parser.add_argument('--lambda_algo', help='algo lambda', type=int, default=100)
    parser.add_argument('--cxpb', '-c', help='crossover proba', type=float, default=0.7)
    parser.add_argument('--mutpb', '-m', help='mutation proba', type=float, default=0.2)
    parser.add_argument('--nbr_items', '-n', help='number of items', type=int, default=10)
    parser.add_argument('--total_price', help='total price', type=int, default=50)
    parser.add_argument('--min_price', help='min price', type=int, default=1)
    parser.add_argument('--max_price', help='max price', type=int, default=10)
    parser.add_argument('--min_quantity', help='min quantity', type=int, default=0)
    parser.add_argument('--max_quantity', help='max quantity', type=int, default=10)
    parser.add_argument('--min_quality', help='min quality', type=int, default=0)
    parser.add_argument('--max_quality', help='max quality', type=int, default=10)
    parser.add_argument('--marging', help='marging (0: disabled)', type=float, default=0.10)
    parser.add_argument('--plot', '-p', help='plot', action='store_true', default=False)
    parser.add_argument('--zero', '-z', help='init solution to zero', action='store_true', default=False)

    parser.add_argument('--algo', '-a', help='algo', default=algorithms.eaMuPlusLambda)
    parser.add_argument('--eaMuPlusLambda', help='eaMuPlusLambda', action='store_const', const=algorithms.eaMuPlusLambda, dest='algo')
    parser.add_argument('--eaMuCommaLambda', help='eaMuCommaLambda', action='store_const', const=algorithms.eaMuCommaLambda, dest='algo')

    parser.add_argument('--entropy', '-e', help='entropy', default=plt.mlab.entropy)
    parser.add_argument('--bins', '-b', help='entropy bins', type=int, default=1)
    parser.add_argument('--matplotlib', help='function plt.mlab.entropy used', action='store_const', const=plt.mlab.entropy, dest='entropy')
    parser.add_argument('--std', help='function numpy.std used', action='store_const', const=lambda x,b: numpy.std(x), dest='entropy')

    parser.add_argument('--pareto', help='pareto', default=tools.selNSGA2)
    parser.add_argument('--selNSGA2', help='selNSGA2', action='store_const', const=tools.selNSGA2, dest='pareto')
    parser.add_argument('--selSPEA2', help='selSPEA2', action='store_const', const=tools.selSPEA2, dest='pareto')

    args = parser.parse_args()

    if args.seed:
        random.seed(args.seed)
        print("seed:", args.seed)

    prices = [random.randint(args.min_price, args.max_price) for _ in range(args.nbr_items)]
    qualities = [random.randint(args.min_quality, args.max_quality) for _ in range(args.nbr_items)]

    creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0, -1.0, 1.0))
    creator.create("Individual", list, fitness=creator.Fitness)

    toolbox = base.Toolbox()

    # Quantity generator
    if args.zero:
        toolbox.register("quantity_item", lambda: args.min_quantity)
    else:
        toolbox.register("quantity_item", random.randint, args.min_quantity, args.max_quantity)

    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.quantity_item, args.nbr_items)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def eval(individual):
        total_price = 0.0
        total_quality = 0.0
        for i in range(args.nbr_items):
            total_price += individual[i] * prices[i]
            total_quality += individual[i] * qualities[i]
        return \
            abs(args.total_price - total_price),\
            args.entropy(individual, args.bins),\
            individual.count(args.min_quantity),\
            total_quality

    def cx(ind1, ind2):
        site = random.randint(0, min(len(ind1), len(ind2)))
        ind1[:site], ind2[:site] = ind2[:site], ind1[:site]
        return ind1, ind2

    def mut(individual):
        pos = random.randint(0, args.nbr_items-1)
        individual[pos] = random.randint(args.min_quantity, args.max_quantity)
        return individual,

    toolbox.register("evaluate", eval)
    toolbox.register("mate", cx)
    toolbox.register("mutate", mut)
    toolbox.register("select", args.pareto)

    pop = toolbox.population(n=args.pop_size)

    # for ind in pop: print(ind)

    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    new_pop, logbook = args.algo(pop, toolbox, args.pop_size, args.lambda_algo, args.cxpb, args.mutpb, args.max_gen, stats, halloffame=hof)

    print(len(hof))
    print(prices)
    print(qualities)

    for x in hof:
        if args.marging:
            if x.fitness.values[0] <= (args.total_price*args.marging):
                print(x, x.fitness)
        else:
            print(x, x.fitness)

    if args.plot:
        gen, avg, min_, max_ = logbook.select("gen", "avg", "min", "max")
        plt.plot(gen, avg, label="average")
        plt.plot(gen, min_, label="minimum")
        plt.plot(gen, max_, label="maximum")
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.legend(loc="lower right")
        plt.show()
