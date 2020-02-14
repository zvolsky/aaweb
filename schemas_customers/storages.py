# Tenant aware storages
# https://github.com/bernardopires/django-tenant-schemas/issues/565

from tenant_schemas.storage import TenantStorageMixin

# original: DEFAULT_FILE_STORAGE = 'django_b2.storage.B2Storage'
from django_b2.storage import B2Storage


# DEFAULT_FILE_STORAGE = 'schemas_customers.storages.TenantB2Storage'
class TenantB2Storage(TenantStorageMixin, B2Storage):
    pass
