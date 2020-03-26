from django import forms
from django.urls import reverse_lazy

from .models import Client


class ClientCreateForm(forms.ModelForm):
    success_url = reverse_lazy('schemas_customers:home')

    class Meta:
        model = Client
        fields = ('schema_name',)
