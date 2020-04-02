import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
#User = get_user_model()
from django.http.response import Http404
from django.shortcuts import redirect  # , render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView, ListView

from .forms import TenantCreateForm
from .models import Tenant


log = logging.getLogger(__name__)


# https://www.agiliq.com/blog/2017/12/when-and-how-use-django-listview/
class TenantList(ListView):
    model = Tenant
    #tenants = Tenant.objects.exclude(name='public').exclude(name='extensions')
    context_object_name = 'clients'
    template_name = "schemas_customers/clients.html"
    paginate_by = 10

    def get_queryset(self):
        clients = Tenant.objects.exclude(name='public')
        for client in clients:
            client.url = '%s://%s' % (self.request.scheme,
                                      '.'.join([client.name] + self.request.get_host().split('.')[-2:]))
        return clients

    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number'] = context['page_obj'].number
        context['num_pages'] = context['paginator'].num_pages

        '''
        clients = Tenant.objects.exclude(name='public')
        for client in clients:
            client.url = '%s://%s' % (self.request.scheme,
                                      '.'.join([client.name] + self.request.get_host().split('.')[-2:]))
        context['clients'] = clients
        '''

        return context
    """

def init_this_project(request):
    host = request.get_host().split(':',1)[:1]
    tenant = Tenant(domain_url=host, schema_name='public', name='public')
    tenant.save()
    return redirect('schemas_customers:clients')


# https://www.agiliq.com/blog/2019/01/django-createview/ (with lot of mistakes)
class TenantCreate(CreateView):
    model = Tenant
    form_class = TenantCreateForm
    template_name = "schemas_customers/tenant_create.html"

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(*args, **kwargs)
        user = self.request.user  # django.contrib.auth.models.AnonymousUser or .User
        if not isinstance(user, get_user_model()):
            messages.error(self.request, _('Cannot create the website: You are not logged in.') +
                    ' <a href="%s">' % reverse("accounts:login") + _('Please log in first.') + '</a>',
                    extra_tags='safe')
            return redirect('schemas_customers:clients')
        return initial

    def form_valid(self, form):
        user = self.request.user  # django.contrib.auth.models.AnonymousUser or .User
        if isinstance(user, get_user_model()):

            self.client = form.save(commit=False)
            self.client.schema_name = self.client.name
            self.client.domain_url = f"{self.client.name}.{'.'.join(self.request.get_host().rsplit('.', 2)[-2:])}"
            self.client.user = user
            self.client.save()
            return redirect(form.success_url)
        else:   # AnonymousUser
            messages.error(self.request, _('Cannot create the website: You are not logged in.') +
                    ' <a href="%s">' % reverse("accounts:login") + _('Please log in first.') + '</a>',
                    extra_tags='safe')
