import os

DOMAIN_NAME = "vegeclic.fr"
ADMIN_EMAIL = "admin@localhost"
ADMIN_PASSWORD = "admin"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "regularcom.settings")

from django.contrib.sites.models import Site

default_site = Site.objects.get(id=1)
default_site.domain = DOMAIN_NAME
default_site.save()

import accounts.models as am

default_account = am.Account.objects.create_superuser(email=ADMIN_EMAIL,
                                                      password=ADMIN_PASSWORD)
