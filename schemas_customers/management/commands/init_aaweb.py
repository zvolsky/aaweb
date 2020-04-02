from django.core.management.base import BaseCommand

from schemas_customers.models import Tenant


class Command(BaseCommand):
    help = "Inicializes aaweb, espec the 1st(public) tenant."

    def add_arguments(self, parser):
        # TODO: make l/d mutually exclusive
        parser.add_argument('-l', '--localhost', action='store_true', default=False,
                help="initialize tenant localhost")
        parser.add_argument('-d', '--domain', type=str,
                help="initialize production tenant (example: aaweb.eu)")

    def handle(self, *_args, **options):
        if not Tenant.objects.exists():
            host = None
            if options['localhost']:
                host = 'localhost'
            elif options['domain']:
                host = options['domain']
            if host:
                tenant = Tenant(domain_url=host, schema_name='public', name='public')
                tenant.save()

                print(f'Public tenant for {host} was initialized.')
        else:
            print("Already initialized, Tenant model isn't empty.")
