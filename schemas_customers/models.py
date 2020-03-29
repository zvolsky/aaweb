from tenant_schemas.models import TenantMixin

from django.contrib.auth import get_user_model
#User = get_user_model()
from django.db import models


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
