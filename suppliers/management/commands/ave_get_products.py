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

def download(url, slug, data=None, filename=None, media_root=settings.MEDIA_ROOT):
    o = parse.urlparse(url).path.split('/')
    dest = '%s/suppliers/product/%s' % (media_root, slug)
    os.makedirs(dest, exist_ok=True)
    dest_path = '%s/%s' % (dest, o[-1] if not filename else filename)
    if os.path.exists(dest_path): return dest_path.replace(settings.MEDIA_ROOT+'/', settings.MEDIA_URL)
    local_path, headers = request.urlretrieve(url, dest_path, data=data)
    # return local_path.replace(settings.MEDIA_ROOT+'/', settings.MEDIA_URL)
    return local_path.replace(settings.MEDIA_ROOT+'/', '')

class Command(NoArgsCommand):
    help = 'Get the AVE supplier products and save it into database'

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

        logging.debug('retrieve suche.html')
        src = bytes()
        if settings.AVE_LOCAL_RETRIEVE:
            src = open('%s/suche.html' % settings.MEDIA_ROOT)
        else:
            src = retrieve('http://shop.ave.vg/shop/suche.html', data=data, limit_size=settings.AVE_LIMIT_SIZE)
        logging.debug('suche.html done')

        logging.debug('apply bs4')
        soup = BeautifulSoup(src)
        logging.debug('bs4 done')

        logging.debug('parse and get the list')
        articles = soup.find_all('div', 'artikel')
        logging.debug('list done')

        logging.debug('num: %d', len(articles))

        updated_data = []

        for article in articles:
            url = article.a['href']
            url_split = url.split('/')
            url_split[-1] = 'index.html'
            url = '/'.join(url_split)

            o = parse.urlparse(url).path.split('/')
            ref = o[3]

            logger_article = logging.getLogger('article %s' % ref)
            logger_db = logging.getLogger('database %s' % ref)

            exist = False
            try:
                price_obj = sm.Price.objects.get(reference=ref)
                logger_db.debug('price object already exists in %s', price_obj)
            except sm.Price.DoesNotExist:
                logger_db.debug('price object doesnot exists yet')
            else:
                exist = True

            logger_article.debug('parsing of brief information from the article %s', ref)

            title = article.a['title']
            thumb = article.a.img['src']
            p = article.find_all('p')
            title2 = p[0].a.text.replace('»', '').strip()
            slug = slugify(title2)
            price = p[1].strong.text.strip()
            weight = p[1].find(text=re.compile('Gewicht')).strip()
            expired = True if article.find(text=re.compile('Derzeit')) else False

            logger_article.debug('parsed data: (%s,%s,%s,%s,%s,%s,%s,%s)', ref, slug, title, thumb, title2, price, weight, expired)

            logger_article.debug('download article %s thumb image', ref)
            thumb_path = download(thumb, slug, data=data)
            logger_article.debug('thumb image %s done', thumb_path)

            logger_article.debug('retrieve article %s', ref)
            article_src = retrieve(url, data=data, limit_size=None, logger=logger_article)
            if not article_src:
                logger_article.debug('article %s failed', ref)
                continue
            logger_article.debug('article %s done', ref)

            logger_article.debug('apply bs4')
            article_soup = BeautifulSoup(article_src)
            logger_article.debug('bs4 done')

            category_obj = None
            category_area = article_soup.find(class_='active')
            if category_area:
                category = category_area.text.title()
                logger_article.debug('category: %s', category)

                try:
                    category_obj = pm.Category.objects.language('de').get(name=category)
                except pm.Category.DoesNotExist:
                    try:
                        category_obj = pm.Category.objects.language('de').get(slug=slugify(category))
                    except pm.Category.DoesNotExist:
                        category_obj = pm.Category.objects.language('de').create(name=category, slug=slugify(category))

            base_product_obj = None

            try:
                base_product_obj = pm.Product.objects.language('de').get(name=category)
            except pm.Product.DoesNotExist:
                try:
                    base_product_obj = pm.Product.objects.language('de').get(slug=slugify(category))
                except pm.Product.DoesNotExist:
                    logger_db.debug('base product object doesnot exists yet')
                    base_product_obj = pm.Product.objects.language('de').create(name=category, slug=slugify(category))
                    base_product_obj.categories.add(category_obj)
                    logger_db.debug('base product object exists now in %s', base_product_obj)
                else:
                    logger_db.debug('base product object already exists in %s', base_product_obj)
            else:
                logger_db.debug('base product object already exists in %s', base_product_obj)

            product_obj = None

            if exist:
                product_obj = sm.Product.objects.language('de').get(price=price_obj)
            else:
                logger_db.debug('check if product already exists thanks to the name')
                try:
                    product_obj = sm.Product.objects.language('de').get(name=title2)
                except sm.Product.DoesNotExist:
                    logger_db.debug('no product found with the name')

                    logger_db.debug('check if product already exists thanks to the slug')
                    try:
                        product_obj = sm.Product.objects.language('de').get(slug=slug)
                    except sm.Product.DoesNotExist:
                        logger_db.debug('no product found with the slug')

                        logger_db.debug('creation of product object in progress')
                        product_obj = sm.Product.objects.language('de').create(name=title2, slug=slug, product=base_product_obj)
                        product_obj.suppliers.add(supplier_obj)
                        logger_db.debug('product object exists now in %s', product_obj)
                        updated_data.append('product %d: a new product has been added. Name: "%s", Category: %s' % (product_obj.id, product_obj.name, base_product_obj.name))
                    else:
                        logger_db.debug('a product already exists with the same slug, we stop here.')
                        exist = True
                else:
                    logger_db.debug('a product already exists with the same name, we stop here.')
                    exist = True

            logger_db.debug('product_obj id is %d' % product_obj.id)

            body = article_soup.find(class_='spalterechts')

            logger_db.debug('creation of thumb image object in progress')
            thumb_obj = cm.Image.objects.create(image=thumb_path, content_type=ContentType.objects.get(app_label='suppliers', model='product'), object_id=product_obj.pk)
            logger_db.debug('thumb image object exists now in %s', thumb_obj)

            if not exist:
                big_img_area = body.find(class_='artikelbild')
                if big_img_area:
                    src = big_img_area.img['src']
                    path = download(src, slug, data=data)
                    logger_article.debug('big_img: %s', path)
                    logger_db.debug('creation of big image object in progress')
                    obj = cm.Image.objects.create(image=path, content_type=ContentType.objects.get(app_label='suppliers', model='product'), object_id=product_obj.pk)
                    logger_db.debug('big image object exists now in %s', obj)
                    product_obj.main_image = obj

                big_img2_area = body.find(id='picture-inner')
                if big_img2_area:
                    objs = []
                    for div in big_img2_area.find_all('div'):
                        src = div.img['src']
                        path = download(src, slug, data=data)
                        logger_article.debug('big_img2_path: %s', path)
                        logger_db.debug('creation of big image (v2) object in progress')
                        obj = cm.Image.objects.create(image=path, content_type=ContentType.objects.get(app_label='suppliers', model='product'), object_id=product_obj.pk)
                        objs += [obj]
                        logger_db.debug('big image (v2) object exists now in %s', obj)
                    if objs:
                        product_obj.main_image = objs[0]

                highres_area = body.find(text=re.compile('Download:'))
                if highres_area:
                    href = highres_area.parent.parent.a['href']
                    path = download(href, slug, data=data, filename='%s.jpg' % ref)
                    logger_article.debug('highres_img_path: %s', path)
                    logger_db.debug('creation of high resolution image object in progress')
                    obj = cm.Image.objects.create(image=path, content_type=ContentType.objects.get(app_label='suppliers', model='product'), object_id=product_obj.pk)
                    logger_db.debug('high resolution image object exists now in %s', obj)

            article_title = body.find(class_='first').text
            article_price = body.find(class_='preis').text
            article_data = body.find(class_='artikelbeschreibung')

            description = article_data.p.text
            product_obj.body = description

            ingredients_area = article_data.find(text=re.compile('Zutaten:'))
            if ingredients_area:
                ingredients = ingredients_area.parent.parent.text
                product_obj.ingredients = ingredients

            number_area = article_data.find(text=re.compile('Art.Nr.:'))
            if number_area:
                number = number_area.parent.next_sibling.strip()
                logger_article.debug('number: %s', number)

            supplier_area = article_data.find(text=re.compile('Hersteller:'))
            if supplier_area:
                supplier = supplier_area.parent.next_sibling.strip()
                logger_article.debug('supplier: %s', supplier)

                try:
                    product_supplier_obj = sm.Supplier.objects.get(slug=slugify(supplier))
                    logger_db.debug('supplier object exists in %s', product_supplier_obj)
                except sm.Supplier.DoesNotExist:
                    product_supplier_obj = sm.Supplier.objects.create(name=supplier, slug=slugify(supplier))
                    supplier_obj.suppliers.add(product_supplier_obj)
                    logger_db.debug('since supplier object doesnot exist yet, it was created in %s', product_supplier_obj)

                product_obj.suppliers.add(product_supplier_obj)

            weight2_area = article_data.find(text=re.compile('Gewicht:'))
            if weight2_area:
                weight2 = weight2_area.parent.next_sibling.strip()
                if weight2 and weight2 != '-':
                    logger_article.debug('weight2: %s', weight2)
                    logger_db.debug('convert weight to float')
                    product_obj.weight = float(weight2.strip().replace(',','.').split(' ')[0])

            price2_area = article_data.find(text=re.compile('Einkaufspreis (EK):'))
            if price2_area:
                price2 = price2_area.parent.next_sibling.strip()
                logger_article.debug('price2: %s', price2)

            package_area = article_data.find(text=re.compile('Verpackungseinheit (VPE):'))
            if package_area:
                package = package_area.parent.next_sibling.strip()
                logger_article.debug('package: %s', package)

            price3_area = article_data.find(text=re.compile('empf. Verkaufspreis (VK):'))
            if price3_area:
                price3 = price3_area.parent.next_sibling.strip()
                logger_article.debug('price3: %s', price3)

            quality_area = article_data.find(text=re.compile('Qualität:'))
            if quality_area:
                quality = quality_area.parent.next_sibling.strip()
                logger_article.debug('quality: %s', quality)

            outofstock_area = article_data.find(text=re.compile('Derzeit leider nicht lieferbar.'))
            if outofstock_area:
                if product_obj.status != 'o':
                    logger_article.debug('out of stock for this article means the status will be changed to out of stock.')
                    updated_data.append('product status changed from %s to outofstock' % product_obj.status)
                    product_obj.status = 'o'
            else:
                if not product_obj.status or product_obj.status in ['o', 'w']:
                    logger_article.debug('article available means the status will be changed to published since it was known as out of stock.')
                    updated_data.append('product status changed from %s to published' % product_obj.status)
                    product_obj.status = 'p'

            logger_article.debug('%s,%s', article_title, article_price)

            product_obj.save()
            logger_db.debug('product object saved')

            logger_db.debug('looking for default currency object')
            currency_obj = cm.Currency.objects.get(name=settings.DEFAULT_CURRENCY)

            logger_db.debug('convert price to float')
            float_price = float(price.split(' ')[1].replace(',', '.'))

            if not exist:
                logger_db.debug('creation of price object in progress')
                price_obj = sm.Price.objects.create(product=product_obj, supplier=supplier_obj, reference=ref, currency=currency_obj, purchase_price=float_price, supplier_product_url=url)
                logger_db.debug('price object exists now in %s', price_obj)
            else:
                if price_obj.purchase_price != float_price:
                    logger_db.debug('new purchase_price updated')
                    updated_data.append('product %d: purchase_price updated. Old: %.2f, New: %.2f' % (product_obj.id, price_obj.purchase_price, float_price))
                    price_obj.purchase_price = float_price
                    price_obj.save()

                if price_obj.reference != ref:
                    logger_db.debug('new reference and url updated')
                    updated_data.append('product %d: reference and url updated. Old: %s, New: %s' % (product_obj.id, price_obj.reference, ref))
                    price_obj.reference = ref
                    price_obj.supplier_product_url = url
                    price_obj.save()

        if updated_data:
            admin = am.Account.objects.get(email=settings.EMAIL_ADMIN)
            mm.Message.objects.create_message(participants=[admin.customer], subject=_("Mise à jour du catalogue"), body=_(
"""Bonjour %(name)s,

Le catalogue a été mis à jour, ci-dessous se trouve la liste des changements opérés :

%(updated_data)s

Bien cordialement,
Végéclic.
"""
            ) % {'name': admin.customer.main_address.__unicode__() if admin.customer.main_address else '',
                 'updated_data': '\n'.join(updated_data)}
            )

        translation.deactivate()
