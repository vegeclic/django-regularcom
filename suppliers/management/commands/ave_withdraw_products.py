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
import mailbox.models as mm
import products.models as pm
import suppliers.models as sm
import common.models as cm
import accounts.models as am
from ... import models
import logging, logging.config

from bs4 import BeautifulSoup
from urllib import request, parse
import sys, os, shutil, re

logging.config.fileConfig('suppliers/management/commands/logging.conf')

def retrieve(url, data=None, chunk_size=settings.AVE_CHUNK, limit_size=settings.AVE_LIMIT_SIZE, logger=logging):
    try:
        src = bytes()
        count = 0

        req = request.Request(url)
        f = request.urlopen(req, data)

        while True:
            chunk = f.read(chunk_size)
            if not chunk: break
            print('.', end='')
            sys.stdout.flush()
            src += chunk
            count += chunk_size
            if limit_size and count >= limit_size: break

        return src
    except UnicodeError:
        logger.critical('unicode error while retrieving the url %s', url)
        return None

class Command(NoArgsCommand):
    help = 'Get the AVE supplier products and save it into database'

    debug = True

    def handle_noargs(self, **options):
        translation.activate('fr')

        logging.debug('Command in progress')

        try:
            supplier_obj = models.Supplier.objects.get(slug=slugify(settings.AVE_SUPPLIER_NAME))
            logging.debug('supplier object exists in %s', supplier_obj)
        except models.Supplier.DoesNotExist:
            supplier_obj = models.Supplier.objects.create(name=settings.AVE_SUPPLIER_NAME, slug=slugify(settings.AVE_SUPPLIER_NAME))
            logging.debug('since supplier object doesnot exist yet, it was created in %s', supplier_obj)

        data = parse.urlencode({'a': 'login',
                                'frm_cid': settings.AVE_LOGIN,
                                'frm_pwd': settings.AVE_PASSWD})
        data = data.encode('utf-8')

        withdrawn_products = []

        for product in models.Product.objects.language('de').all():
            price = product.price_set.get(supplier=supplier_obj)
            ref = price.reference
            url = price.supplier_product_url

            logger_article = logging.getLogger('article %s' % ref)
            logger_db = logging.getLogger('database %s' % ref)

            logger_article.debug('retrieve article %s', ref)
            article_src = retrieve(url, data=data, limit_size=None, logger=logger_article)
            if not article_src:
                logger_article.debug('article %s failed', ref)
                continue
            logger_article.debug('article %s done', ref)

            logger_article.debug('apply bs4')
            article_soup = BeautifulSoup(article_src)
            logger_article.debug('bs4 done')

            body = article_soup.find(class_='spalterechts')
            article_title = body.find(class_='first').text

            if article_title: continue

            logger_db.debug('changed the status of product %d to withdrawn' % product.id)

            product.status = 'w'
            product.save()

            withdrawn_products.append("%d: %s" % (product.id, product.name))

        if withdrawn_products:
            admin = am.Account.objects.get(email=settings.EMAIL_ADMIN)
            mm.Message.objects.create_message(participants=[admin.customer], subject=_("Produits retirés du catalogue"), body=_(
"""Bonjour %(name)s,

Le catalogue a été mis à jour, certains produits ont été retirés du catalogue, voici la liste :

%(withdrawn_products)s

Bien cordialement,
Végéclic.
"""
            ) % {'name': admin.customer.main_address.__unicode__() if admin.customer.main_address else '',
                 'withdrawn_products': '\n'.join(withdrawn_products)}
            )

        translation.deactivate()
