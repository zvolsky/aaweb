from django.contrib import admin

from .models import Tenant


@admin.register(Tenant)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain_url', 'schema_name', 'name', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'schema_name', 'domain_url')
