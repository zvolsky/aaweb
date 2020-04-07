import base64

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from schemas_customers.models import Tenant


class Command(BaseCommand):
    help = "Inicializes tenant ie. creates a new postgres db schema. WIthout params: list subdomains."
    example = "(example: aaweb.eu, localhost)"

    def add_arguments(self, parser):
        parser.add_argument('-d', '--domain', type=str,
                help=f"2nd level domain name {self.example}")
        parser.add_argument('-s', '--subdomain', type=str,
                help="3rd level name (ommit basic 2nd level domain name): initialize tenant with this name")
        parser.add_argument('-u', '--userid', type=int,
                help="user id of the user asking for new tenant")
        parser.add_argument('-l', '--description-delimited', type=str,
                help="description, you can use string delimiters \"..\" and escape \\\" if necessary")
        parser.add_argument('-b', '--description-base64', type=str,
                help="description, use base64.b64encode()")

    def handle(self, *_args, **options):
        domain = options['domain']
        subdomain = options['subdomain']
        if domain and subdomain:
            if subdomain not in ('public', 'extensions', 'www') and not Tenant.objects.filter(name=subdomain).exists():
                desc = options.get('description_base64')
                if desc:
                    desc = base64.b64decode(desc).decode()
                else:
                    desc = options.get('description_delimited')  # escapes in "..." are handled automatically
                if desc:
                    user = options.get('userid')
                    if user:
                        user = get_user_model().objects.get(id=user)
                    full = '%s.%s' % (subdomain, domain)
                    tenant = Tenant(domain_url=full, schema_name=subdomain, name=subdomain,
                            user=user, description=desc)
                    tenant.save()
                    # here ~ a minute run migrations for the new tenant
                    tenant.created_on = now()
                    tenant.save()  # and here we give information that the tenant is ready
                    print(f'Tenant {full} was initialized.')
                else:
                    print('Use -l or -b for tenant description.')
            else:
                print(f"Subdomain {subdomain} is in use.")
        else:
            print("Active domains:")
            tenants = Tenant.objects.exclude(name='public')
            if tenants:
                for subdomain in tenants:
                    print(f'  {subdomain}')
            else:
                print('  no subdomain yet')
            print(f"Use both -s and -d {self.example} parameters to create new subdomain.")
