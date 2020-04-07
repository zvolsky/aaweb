from django import forms
#from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
#from django.utils.translation import gettext_lazy as _

from .models import Tenant


class TenantCreateForm(forms.ModelForm):
    success_url = reverse_lazy('schemas_customers:creating')

    class Meta:
        model = Tenant
        fields = ('name', 'description')
