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
from django.utils.text import slugify
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
import products.models as pm
from ... import models
import logging, logging.config
import readline

import re, sys
from pyparsing import *

logging.config.fileConfig(settings.BASE_DIR + '/suppliers/management/commands/logging.conf')

class Command(NoArgsCommand):
    help = 'Converter of the ingredients list'

    def handle_noargs(self, **options):
        translation.activate('fr')
        logging.debug('Command in progress')

        zutaten = CaselessLiteral('Zutaten:')
        nahrwerte = CaselessLiteral('Nährwerte pro 100g:')
        allergiehinweis = (CaselessLiteral('Allergiehinweis:') | CaselessLiteral('Allergikerhinweis:'))
        asterisk = Literal('*')
        comma = Literal(',')
        percent = Literal('%')
        lpar  = Literal('(').suppress()
        rpar  = Literal(')').suppress()
        equal = Literal('=')
        point = Word('.,')
        dot = Word('.').suppress()
        colons = Literal(':').suppress()
        number = Word(nums)
        integer = number
        floatnumber = Combine(integer + Optional(point + Optional(number)))
        extent = Optional(lpar).suppress() + Combine(floatnumber + percent) + Optional(rpar).suppress()
        term = Word(alphas + alphas8bit + '-. ')
        emulgator = (lpar + Combine(CaselessLiteral('E') + number) + rpar)

        ingredients = Forward()
        ingredient = term + Optional(emulgator) + Optional(asterisk)
        ingredients << delimitedList(Group((ingredient + Optional(extent)).setParseAction(lambda s,l,t: (t[0], t[1:])) + Optional(lpar + ingredients + rpar)), comma)
        ingredient_stmt = zutaten.suppress() + Group(ingredients).setResultsName('ingredients') + Optional(dot).suppress()

        bio_asterisk_stmt = Optional(lpar) + asterisk + Optional(equal) + (CaselessLiteral('aus kontrolliert biologischem Anbau') | CaselessLiteral('aus ökologischem Landbau') | CaselessLiteral('aus biologischem Anbau')) + Optional(rpar)

        kj = (floatnumber + CaselessLiteral('KJ')).setParseAction(lambda s,l,t: ''.join(t)) + Literal('/').suppress() + (floatnumber + CaselessLiteral('kcal')).setParseAction(lambda s,l,t: ''.join(t))
        gram = (Optional(Word('<>')) + floatnumber + (Literal('g') | Literal('kg'))).setParseAction(lambda s,l,t: ''.join(t))
        energy = (term + Optional(colons) + Optional(kj | gram) + Optional(lpar + SkipTo(rpar) + rpar)).setParseAction(lambda s,l,t: [t])
        energies = delimitedList(energy, comma)
        energy_stmt = nahrwerte.suppress() + Group(energies).setResultsName('energies') + Optional(dot)

        allergie = Word(alphas + alphas8bit + '-').setParseAction(lambda s,l,t: t[0])
        allergies = delimitedList(allergie, comma)
        allergie_stmt = allergiehinweis.suppress() + Group(allergies).setResultsName('allergies') + Optional(dot)

        extras_default_data = {'glutenFree': False, 'cacaoExtent': None}
        extras = {}

        def setCacaoExtent(s,l,t):
            extras['cacaoExtent'] = t[1]
            return t

        glutenfree_stmt = Combine(CaselessLiteral('Ohne Gluten') + restOfLine)
        cacaoextent_stmt = (CaselessLiteral('Kakao mindestens') + extent).setParseAction(setCacaoExtent) + Optional(restOfLine)
        laxative_stmt = CaselessLiteral('Kann bei') + Optional(restOfLine)
        traces_stmt = Combine(CaselessLiteral('Dieses Produkt') + restOfLine)

        def setGlutenFree(s,l,t):
            print('setGlutenFree')
            extras['glutenFree'] = True
            return t

        bnf = (ingredient_stmt + Optional(bio_asterisk_stmt).suppress())\
              + Optional(glutenfree_stmt.setParseAction(setGlutenFree))\
              + Optional(cacaoextent_stmt).suppress()\
              + Optional(laxative_stmt).suppress()\
              + Optional(traces_stmt).suppress()\
              + Optional(energy_stmt)\
              + Optional(allergie_stmt)\

        pattern = bnf + StringEnd()

        import pprint
        pp = pprint.PrettyPrinter(2)

        print("Usage:")
        print("* [CTRL+C] to skip current ingredients list")
        print("* [CTRL+D] to stop program")

        for p in models.Product.objects.exclude(brut_ingredients_de='').all():
            extras.update(extras_default_data)

            print("\n### Parsing of %d, %s ###\n" % (p.id, p.name))

            ingredients = p.brut_ingredients_de
            updated = False

            while True:
                try:
                    try:
                        print('= Suggestion =\n%s\n' % ingredients.replace("\r\n", '[NL]').replace("\n", '[NL]'))
                        d = pattern.parseString(ingredients)
                        pp.pprint(d.asList())
                        print(extras)
                        if not updated: break
                        if input('\n[%d, %s] [(Y)es/(N)o ?]$ ' % (p.id, p.name)).lower() == 'y':
                            p.brut_ingredients_de = ingredients
                            p.save()
                            break
                    except ParseException as err:
                        print('= Error =')
                        print(err.line)
                        print(' ' * (err.col-1) + '^')
                        print(err)
                        print('= End of error =\n')

                    ingredients = None
                    while not ingredients:
                        ingredients = input('[%d, %s] [new ingredients]$ ' % (p.id, p.name))
                        ingredients = ingredients.replace('[NL]', "\n")
                        updated = True
                except KeyboardInterrupt:
                    print('\n\n= Canceled =')
                    break

        translation.deactivate()
