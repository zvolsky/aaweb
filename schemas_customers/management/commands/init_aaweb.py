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

        parser.add_argument('-t', '--test', type=str)

    def handle(self, *_args, **options):
        if options['test']:
            from tenant_schemas.utils import schema_context
            from django.contrib.auth import get_user_model
            import pdb; pdb.set_trace()

            with schema_context('public'):
                user = get_user_model().objects.get(pk=1)
            with schema_context('muzy'):
                if not get_user_model().objects.exists():
                    user.pk = None
                    user.save()


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
                print('Use -l or -d parameter.')
        else:
            print("Already initialized, Tenant model isn't empty.")
