from tenant_schemas.models import TenantMixin

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
#User = get_user_model()
from django.db import models
from django.utils.translation import gettext_lazy as _


def validate_tenant_name(value):
    if value in ('www', 'public', 'extensions'):
        raise ValidationError(_('This name is reserved.'), code='name_reserved')


class Tenant(TenantMixin):
    name = models.SlugField(_('name'), max_length=100, unique=True, validators=[validate_tenant_name])
    description = models.TextField(_('description'))
    created_on = models.DateField(null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    publicly = models.BooleanField(_('I agree that the link to my website can be publicly shown on main page of this web.'), default=True)

    def __str__(self):
        return self.name
