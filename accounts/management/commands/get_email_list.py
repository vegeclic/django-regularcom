from ... import models
from django.core.management.base import BaseCommand, CommandError, NoArgsCommand

class Command(NoArgsCommand):
    help = 'Get a list of the accounts email'

    def handle_noargs(self, **options):
        for a in models.Account.objects.all():
                print(a.email, end=' ')

